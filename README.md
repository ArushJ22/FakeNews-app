# 📰 Fake News Detection App

This is a full-stack Fake News Detection web application powered by a fine-tuned BERT model. It allows users to detect whether a news article is **real** or **fake** using a clean and intuitive interface.

## 🚀 Features

- ✅ BERT-based ML model for fake news classification  
- ✅ FastAPI backend with REST API endpoints  
- ✅ Simple frontend (HTML/CSS/JS)  
- ✅ Dockerized for easy deployment  
- ✅ Integration & edge case testing scripts included  

## 🧠 Model Info

- Trained on ISOT & LIAR datasets  
- Fine-tuned using Hugging Face’s `bert-base-uncased`  
- Tokenizer + config files included  
- Prediction via `predict_label()` function in `main.py`  

## 🧪 Testing

Run all tests with:

```bash
pytest tests/
python test_integration.py
python edge_test.py
```

## 🐳 Docker

Build and run:

```bash
docker rm -f fakenews-container
docker build -t fakenews-api .
docker run -d -p 8000:8000 --name fakenews-container fakenews-api
```

## 🌐 Deployment

This app can be deployed using **Render**, **Railway**, or **AWS EC2**.

## ✨ Credits

- Hugging Face Transformers  
- TensorFlow  
- FastAPI  
- Docker  

## 📬 Contact

**Arush John**  
GitHub: [@ArushJ22](https://github.com/ArushJ22)
