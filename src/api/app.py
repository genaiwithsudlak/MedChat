# src/api/app.py
from fastapi import FastAPI
from src.utils.logger import logger
from src.api.routes import router as api_router

def create_app():
    app = FastAPI(title="Medical Chatbot API")
    app.include_router(api_router)
    logger.info("API app created")
    return app

# If executed directly by uvicorn: uvicorn src.api.app:create_app
