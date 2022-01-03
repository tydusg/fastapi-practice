from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

dbname = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
user_pass = os.environ.get("DB_USER_PASS")
hostname = os.environ.get("DB_HOSTNAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{user_pass}@{hostname}/{dbname}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
