# backend/services/llm_service.py
from src.utils.logger import logger
from typing import Any

def answer_question(question: str) -> str:
    logger.info("LLM service called", extra={"question_len": len(question)})
    try:
        # example: call src.services.llm_service (or src.llm.openai_llm)
        from src.services.llm_service import answer_question as svc_answer
        resp = svc_answer(question)
        logger.debug("LLM returned response", extra={"response_preview": (resp[:200] if isinstance(resp, str) else str(resp)[:200])})
        return resp
    except Exception as e:
        logger.exception("LLM service failed")
        raise
