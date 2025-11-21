# src/processing/embeddings_generator.py
from src.utils.logger import logger

def generate_embeddings(docs):
    logger.info("Generating embeddings", extra={"num_docs": len(docs)})
    try:
        # call sentence-transformers etc
        embeddings = ["emb_stub" for _ in docs]
        logger.info("Embeddings generated", extra={"count": len(embeddings)})
        return embeddings
    except Exception:
        logger.exception("Embedding generation failed")
        raise
