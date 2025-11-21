# src/ingestion/pdf_to_text.py
"""
Robust PDF -> text loader.

- Accepts a path or a filename located in data/raw/
- If extension omitted, tries .pdf
- Returns extracted text and the resolved Path object (useful for metadata)
"""
from pathlib import Path
from typing import Tuple
import pdfplumber
from ..utils.logger import get_logger

logger = get_logger(__name__)

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

def _resolve_pdf_path(input_path: str) -> Path:
    p = Path(input_path)
    # if user gave a name without extension and it's not an absolute path, try .pdf in raw dir
    if not p.suffix:
        candidates = [
            Path(input_path).with_suffix(".pdf"),
            RAW_DIR / f"{input_path}.pdf",
            RAW_DIR / input_path  # in case provided subpath under raw
        ]
    else:
        candidates = [p, RAW_DIR / p.name, p.resolve()]

    for c in candidates:
        if c.exists():
            return c.resolve()
    # if none found, raise with helpful message
    tried = ", ".join(str(x) for x in candidates)
    raise FileNotFoundError(f"PDF not found. Tried: {tried}")

def pdf_to_text(input_path: str, return_path: bool = False) -> Tuple[str, Path]:
    """
    Extract text from PDF. Returns (text, resolved_path) if return_path True,
    otherwise returns text only.
    """
    pdf_path = _resolve_pdf_path(input_path)
    logger.info("Opening PDF: %s", pdf_path)
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text() or ""
                except Exception as exc:
                    logger.warning("Failed to extract text on page %s: %s", i, exc)
                    text = ""
                pages.append(text)
    except Exception as exc:
        logger.exception("Failed to open PDF %s: %s", pdf_path, exc)
        raise

    full_text = "\n".join(pages)
    logger.info("Extracted %d characters from %s", len(full_text), pdf_path.name)
    if return_path:
        return full_text, pdf_path
    return full_text, pdf_path
