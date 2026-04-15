from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import time
import logging

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/prompt_db"
)

# pool_pre_ping helps detect dead connections
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def wait_for_db(max_retries=15, delay=3):
    """Wait until PostgreSQL is ready to accept connections"""
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))   # <-- Fixed with text()
            logging.info("✅ Database is ready!")
            return True
        except Exception as e:
            logging.warning(f"⏳ Waiting for database... attempt {i+1}/{max_retries} (Error: {type(e).__name__})")
            time.sleep(delay)
    raise Exception("❌ Could not connect to database after retries")