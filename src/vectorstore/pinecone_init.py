# src/vectorstore/pinecone_init.py
"""
Optional Pinecone init. If pinecone not installed or env missing, returns None.
"""
# src/vectorstore/pinecone_init.py
import os
from ..utils.logger import logger
from ..utils.config import get_pinecone_config

def init_pinecone_client():
    try:
        import pinecone
    except Exception:
        logger.debug("pinecone package not available")
        return None

    cfg = get_pinecone_config()
    api_key = os.environ.get(cfg.get("api_key_env_var", "PINECONE_API_KEY"))
    env = os.environ.get(cfg.get("environment_env_var", "PINECONE_ENV"))
    index_name = os.environ.get(cfg.get("index_name_env_var", "PINECONE_INDEX_NAME"))

    if not api_key or not env or not index_name:
        logger.info("Pinecone environment variables not set; skipping pinecone init")
        return None

    pinecone.init(api_key=api_key, environment=env)
    if index_name not in pinecone.list_indexes():
        # default dimension unknown; user must create or ensure dims match
        logger.info("Creating pinecone index: %s", index_name)
        pinecone.create_index(index_name, dimension=1536)
    index = pinecone.Index(index_name)
    logger.info("Pinecone initialized with index: %s", index_name)
    return index
