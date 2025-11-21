# src/retrieval/retriever.py
"""
Simple local vector-based retriever using numpy and cosine similarity.
Exports:
- embed_and_retrieve(query_text, top_k)
- retrieve_by_embedding(embedding, top_k)
"""
# src/retrieval/retriever.py
from typing import List, Dict, Tuple
import numpy as np
from numpy.linalg import norm
from ..utils.helpers import read_json, read_numpy_array
from ..utils.logger import logger
from ..llm.openai_llm import embed_text
import os

EMB_REL = "embeddings/embeddings.npy"
META_REL = "processed/chunks_metadata.json"

def _load_local_store() -> Tuple[np.ndarray, List[Dict]]:
    arr = read_numpy_array(EMB_REL)
    metas = read_json(META_REL)
    return arr, metas

def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (norm(a) * norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def retrieve_by_embedding(query_embedding: List[float], top_k: int = 3) -> List[Dict]:
    arr, metas = _load_local_store()
    q = np.asarray(query_embedding, dtype=np.float32)
    # normalize to avoid repeated norms
    arr_norms = np.linalg.norm(arr, axis=1)
    q_norm = np.linalg.norm(q)
    if q_norm == 0:
        logger.warning("Query embedding has zero norm")
        scores = [(i, 0.0) for i in range(arr.shape[0])]
    else:
        # vectorized cosine
        dots = arr.dot(q)
        denom = arr_norms * q_norm
        # avoid divide by zero
        denom[denom == 0] = 1e-10
        scores = [(int(i), float(dots[i] / denom[i])) for i in range(arr.shape[0])]
    scores.sort(key=lambda x: x[1], reverse=True)
    results = []
    for idx, score in scores[:top_k]:
        m = metas[idx].copy()
        m["score"] = float(score)
        results.append(m)
    logger.info("Retrieval returned %d results (top_k=%d)", len(results), top_k)
    return results

def embed_and_retrieve(query_text: str, top_k: int = 3):
    model = os.environ.get("EMBEDDINGS_MODEL")
    emb = embed_text(query_text, model=model)
    return retrieve_by_embedding(emb, top_k=top_k)
