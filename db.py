from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

GCLOUD_DB_PASS = os.getenv('GCLOUD_DB_PASS')
GCLOUD_IP_ADDR= os.getenv('GCLOUD_IP_ADDR')
SQLALCHEMY_DB_URL = f'postgresql://postgres:{GCLOUD_DB_PASS}@{GCLOUD_IP_ADDR}:5432/postgres'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)