from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from sqlmodel import Session, select
from models import Article
from database import create_db_and_tables, engine
import joblib

from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load saved BERT model and tokenizer (binary classification)
from transformers import AutoTokenizer, AutoConfig, BertForSequenceClassification

config = AutoConfig.from_pretrained("best_model_bert")
model_bert = BertForSequenceClassification.from_pretrained(
    "best_model_bert",
    config=config
)
tokenizer_bert = AutoTokenizer.from_pretrained("best_model_bert")
model_bert.eval()

# Load saved SVM model (TF-IDF + classifier pipeline)
#svm_pipeline = joblib.load("svm_model.pkl")

# Updated Label mapping: Binary classification
label_map = {
    0: "fake",
    1: "real"
}

app = FastAPI()

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 HTML templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Serve home page
@app.get("/", response_class=HTMLResponse)
def serve_home():
    html_path = Path("templates/index.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)

# --- Request Body Models ---
class ArticleInput(BaseModel):
    content: str

class ArticleURLInput(BaseModel):
    url: str

# --- ML Prediction Function ---
def predict_label(content: str) -> str:
    
    inputs = tokenizer_bert(content, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model_bert(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return label_map[predicted_class]
    
    #pred = svm_pipeline.predict([content])[0]
    #return label_map[pred]

# --- API Endpoints ---
@app.post("/articles/")
def create_article(article_input: ArticleInput):
    label = predict_label(article_input.content)
    article = Article(content=article_input.content, label=label)
    with Session(engine) as session:
        session.add(article)
        session.commit()
        session.refresh(article)
    return {
        "id": article.id,
        "label": label,
        "message": "Article analyzed and saved"
    }

@app.post("/articles/from_url/")
def create_article_from_url(article_url: ArticleURLInput):
    try:
        response = requests.get(article_url.url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        content = ' '.join([p.get_text() for p in soup.find_all('p')])
        if not content.strip():
            raise HTTPException(status_code=400, detail="No content found at URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch or parse URL: {e}")

    label = predict_label(content)
    article = Article(content=content, label=label)
    with Session(engine) as session:
        session.add(article)
        session.commit()
        session.refresh(article)
    return {
        "id": article.id,
        "label": label,
        "message": "Article from URL analyzed and saved"
    }

@app.get("/articles/")
def read_articles():
    with Session(engine) as session:
        return session.exec(select(Article)).all()
