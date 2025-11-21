# src/services/llm_service.py
from src.utils.logger import logger
from typing import Any

def answer_question(question: str) -> str:
    logger.info("src.services.llm_service.answer_question called", extra={"q_len": len(question)})
    try:
        # placeholder for actual LLM code using langchain/openai
        response = f"Echo (dev): {question}"
        logger.debug("LLM built response", extra={"resp_preview": response[:200]})
        return response
    except Exception:
        logger.exception("Failed to answer question")
        raise
