# src/utils/config.py

import os
import yaml
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # load .env file


CONFIG_DIR = Path("config")


# -----------------------------
# Data Classes for Structured Config
# -----------------------------
@dataclass
class OpenAIConfig:
    api_key: str
    embedding_model: str
    chat_model: str


@dataclass
class PineconeConfig:
    api_key: str
    environment: str
    index_name: str


@dataclass
class AppConfig:
    project_name: str
    log_level: str


# -----------------------------
# Utility Loader
# -----------------------------
def load_yaml(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing config: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -----------------------------
# OpenAI Config Loader
# -----------------------------
def load_openai_config() -> OpenAIConfig:
    cfg_path = CONFIG_DIR / "openai_config.yaml"
    data = load_yaml(cfg_path)

    return OpenAIConfig(
        api_key=os.getenv("OPENAI_API_KEY") or data.get("api_key"),
        embedding_model=data.get("embedding_model", "text-embedding-3-large"),
        chat_model=data.get("chat_model", "gpt-4.1")
    )


# -----------------------------
# Pinecone Config Loader
# -----------------------------
def load_pinecone_config() -> PineconeConfig:
    cfg_path = CONFIG_DIR / "pinecone_config.yaml"
    data = l
