# src/llm/openai_llm.py
from src.utils.logger import logger
import os
# Actual code should use openai or langchain; keep secrets out of logs.

def call_openai(prompt: str) -> str:
    logger.info("Calling OpenAI", extra={"prompt_len": len(prompt)})
    # Example stub
    try:
        # real call: client = OpenAI(...) etc
        result = f"OpenAI stub for: {prompt[:100]}"
        logger.debug("OpenAI returned", extra={"preview": result[:200]})
        return result
    except Exception:
        logger.exception("OpenAI call failed")
        raise
