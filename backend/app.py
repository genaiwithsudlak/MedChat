# backend/app.py
from fastapi import FastAPI, Request
from backend.routes.chatbot_routes import router as chatbot_router
from backend.utils.logger import logger
import time

def create_app() -> FastAPI:
    app = FastAPI(
        title="Medical Chatbot Backend",
        version="1.0",
        description="Backend API for Medical Chatbot with RAG + LLM",
    )

    # Register routes
    app.include_router(chatbot_router, prefix="/api")

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        logger.info(f"HTTP START: {request.method} {request.url}")
        try:
            response = await call_next(request)
            elapsed = (time.time() - start_time) * 1000
            logger.info(f"HTTP END: {request.method} {request.url} status={response.status_code} time_ms={elapsed:.1f}")
            return response
        except Exception:
            logger.exception("Unhandled exception in request")
            raise

    logger.info("Backend FastAPI application initialized.")
    return app

app = create_app()
