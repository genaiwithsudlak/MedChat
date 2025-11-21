# src/llm/prompt_template.py
from typing import List, Dict

def build_rag_prompt(query: str, context_chunks: List[Dict], max_context_chars: int = 3000) -> str:
    """
    Build RAG prompt that includes context chunks and user query.
    Limits total context characters to max_context_chars (approx).
    """
    header = (
        "You are a precise, careful medical research assistant. "
        "Answer using only the provided context. If the answer is not present in the context, "
        "respond: 'I don't know based on the provided sources.'\n\n"
    )
    selected = []
    total = 0
    for c in context_chunks:
        piece = c.get("text", "")
        if not piece:
            continue
        if total + len(piece) > max_context_chars and selected:
            break
        selected.append(piece)
        total += len(piece)

    ctx = "\n\n---\n\n".join(selected) if selected else ""
    prompt = f"{header}Context:\n{ctx}\n\nQuestion:\n{query}\n\nAnswer:"
    return prompt
