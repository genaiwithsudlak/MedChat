# src/llm/rag_chain.py
from typing import Dict, Any
from ..retrieval.retriever import embed_and_retrieve
from ..llm.prompt_template import build_rag_prompt
from ..llm.openai_llm import chat_completion
from ..utils.logger import logger

def answer_query(query: str, top_k: int = 3, temperature: float = 0.0) -> Dict[str, Any]:
    """
    Full RAG: retrieve -> build prompt -> LLM -> return answer + sources
    """
    # 1) retrieve
    ctx = embed_and_retrieve(query, top_k=top_k)
    if not ctx:
        logger.warning("No context retrieved for query")
    # 2) build prompt
    prompt = build_rag_prompt(query, ctx)
    # 3) call LLM
    try:
        answer = chat_completion(system="You are a helpful assistant.", user=prompt, temperature=temperature)
    except Exception as exc:
        logger.exception("LLM call failed: %s", exc)
        raise
    return {"answer": answer, "sources": ctx}
