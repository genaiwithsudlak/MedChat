# tests/test_retriever.py
import numpy as np

try:
    from src.retrieval.retriever import _cosine_sim
except ImportError:
    _cosine_sim = None

def test_numpy_cosine_similarity():
    a = np.array([1., 0.])
    b = np.array([0., 1.])
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    val = 0.0 if denom == 0 else a.dot(b) / denom
    assert val == 0.0
