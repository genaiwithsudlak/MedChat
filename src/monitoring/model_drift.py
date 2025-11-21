# src/monitoring/model_drift.py
import numpy as np
from typing import Dict, Any

def embedding_stats(embeddings: np.ndarray) -> Dict[str, Any]:
    norms = np.linalg.norm(embeddings, axis=1)
    return {
        "count": int(embeddings.shape[0]),
        "dim": int(embeddings.shape[1]),
        "mean_norm": float(norms.mean()),
        "std_norm": float(norms.std())
    }
