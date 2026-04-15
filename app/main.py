from fastapi import FastAPI
from app.db.database import engine, Base, wait_for_db
from app.routers.prompts import router
import logging

app = FastAPI(
    title="Prompt Versioning System (Llama 3.1:8B)",
    version="1.0"
)

@app.on_event("startup")
def startup_event():
    logging.info("🚀 Starting application...")
    wait_for_db()                    # Wait for Postgres
    Base.metadata.create_all(bind=engine)   # Create tables
    logging.info("✅ Database tables created (if not exist)")

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "✅ Prompt Versioning System with Llama 3.1:8B is running!",
        "docs": "http://localhost:8000/docs"
    }