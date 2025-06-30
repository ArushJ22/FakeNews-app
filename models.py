from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    label: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    article_id: int = Field(foreign_key="article.id")
    confidence: float
    risk_level: str
    source_credibility: str

class UserFeedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    article_id: int = Field(foreign_key="article.id")
    user: str
    feedback: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str  # 'admin', 'moderator', 'analyst'
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)
