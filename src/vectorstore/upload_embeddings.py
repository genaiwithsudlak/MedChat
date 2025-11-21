# src/vectorstore/upload_embeddings.py
"""
Upload local embeddings to pinecone (if enabled). Safe-guarded; no-op if pinecone not configured.
"""
# src/vectorstore/upload_embeddings.py
from ..vectorstore.pinecone_init import init_pinecone_client
from ..utils.helpers import read_json, read_numpy_array
from ..utils.logger import logger

BATCH_SIZE = 100

def upload_to_pinecone():
    idx = init_pinecone_client()
    if not idx:
        logger.info("Pinecone not initialized; skipping upload")
        return False

    metas = read_json("processed/chunks_metadata.json")
    arr = read_numpy_array("embeddings/embeddings.npy")
    # upsert expects list of (id, vector, metadata)
    vectors = []
    for i, meta in enumerate(metas):
        vec = arr[i].astype(float).tolist()
        vectors.append((str(meta["id"]), vec, {"text": meta.get("text",""), "source": meta.get("source", "")}))

    for i in range(0, len(vectors), BATCH_SIZE):
        batch = vectors[i:i+BATCH_SIZE]
        idx.upsert(vectors=batch)
        logger.info("Uploaded batch %d - %d", i, i+len(batch))
    logger.info("Uploaded %d vectors to Pinecone", len(vectors))
    return True

if __name__ == "__main__":
    upload_to_pinecone()
