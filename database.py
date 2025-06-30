from sqlmodel import SQLModel, create_engine
from models import Article

# Create a SQLite database named 'fakenews.db'
sqlite_file_name = "fakenews.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
