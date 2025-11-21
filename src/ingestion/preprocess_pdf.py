# src/ingestion/preprocess_pdf.py
"""
Main preprocessing script.

Usage:
    python -m src.ingestion.preprocess_pdf --pdf Medical_book

Outputs (per PDF):
    data/processed/{pdf_name}/raw_text.json       -- raw cleaned full text (for debugging)
    data/processed/{pdf_name}/entries.json        -- list of chunk objects (id, content, source, char_count)
"""
import argparse
import json
from pathlib import Path
from ..processing.splitter import split_into_chunks
from .pdf_to_text import pdf_to_text
from .text_cleaning import clean_text
from ..utils.logger import get_logger

logger = get_logger(__name__)

BASE_PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"

def _safe_name(name: str) -> str:
    # remove extension if provided, sanitize spaces
    p = Path(name).stem
    return p.replace(" ", "_")

def run(pdf: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Run full preprocess for `pdf` (path or filename in data/raw).
    Saves output to: data/processed/{pdf_name}/entries.json
    """
    logger.info("Starting preprocessing for: %s", pdf)
    text, resolved_path = pdf_to_text(pdf, return_path=True)
    source_name = resolved_path.name
    cleaned = clean_text(text, keep_paragraphs=True)

    pdf_key = _safe_name(resolved_path.stem)
    out_dir = BASE_PROCESSED / pdf_key
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save cleaned raw text for debugging
    raw_out = out_dir / "raw_text.json"
    with open(raw_out, "w", encoding="utf-8") as f:
        json.dump({
            "source": str(resolved_path),
            "length_chars": len(cleaned),
            "text": cleaned
        }, f, indent=2)
    logger.info("Saved cleaned raw text -> %s", raw_out)

    # Chunking using hybrid sentence grouping
    chunks = split_into_chunks(cleaned, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    entries = []
    for i, c in enumerate(chunks):
        entries.append({
            "id": i,
            "content": c,
            "source": source_name,
            "char_count": len(c)
        })

    entries_out = out_dir / "entries.json"
    with open(entries_out, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    logger.info("Saved %d chunks -> %s", len(entries), entries_out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", "-p", required=True, help="PDF path or filename (if in data/raw omit path)")
    parser.add_argument("--chunk_size", type=int, default=1000)
    parser.add_argument("--chunk_overlap", type=int, default=200)
    args = parser.parse_args()
    run(args.pdf, chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap)
