# backend/routes/chatbot_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.utils.logger import logger
from typing import Any

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask(req: ChatRequest) -> Any:
    logger.info("Received chat request")
    try:
        # import service inside to avoid circular imports at startup
        from backend.services.llm_service import answer_question
        answer = answer_question(req.question)
        logger.info("Answered question successfully")
        return {"answer": answer}
    except Exception as e:
        logger.exception("Error while answering")
        raise HTTPException(status_code=500, detail="Internal server error")
