# src/ingestion/text_cleaning.py
"""
Lightweight PDF text cleaner. Keeps medical text intact while removing unusual control characters,
normalizing whitespace and linebreaks, and preserving paragraphs.
"""
import re
from ..utils.logger import get_logger

logger = get_logger(__name__)

def clean_text(text: str, keep_paragraphs: bool = True) -> str:
    if text is None:
        return ""
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Replace multiple form-feeds / weird pages separators with double newline
    text = re.sub(r"\f+", "\n\n", text)
    # Remove non-printable characters except newlines and tabs
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u00A0-\u024F]+", " ", text)
    # Collapse multiple spaces but keep paragraph breaks
    if keep_paragraphs:
        parts = [re.sub(r"[ \t]+", " ", p).strip() for p in text.split("\n\n")]
        cleaned = "\n\n".join([p for p in parts if p])
    else:
        cleaned = re.sub(r"[ \t\n]+", " ", text).strip()
    logger.info("Cleaned text length: %d", len(cleaned))
    return cleaned
