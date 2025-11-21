# src/processing/splitter.py
"""
Hybrid (Option D) chunking: sentence-tokenize then group sentences to reach a target
chunk size in characters, with chunk overlap.

Exports:
- split_into_chunks(text, chunk_size=1000, chunk_overlap=200) -> List[str]

Behavior:
- Uses NLTK punkt sentence tokenizer.
- Groups consecutive sentences into chunks aiming for chunk_size characters.
- Ensures chunk overlap by carrying last sentences such that overlap (in chars) >= chunk_overlap.
"""
from typing import List
import nltk
from ..utils.logger import get_logger

from src.utils.nltk_setup import ensure_nltk
ensure_nltk()


logger = get_logger(__name__)

# Ensure punkt tokenizer is available
try:
    nltk.data.find("tokenizers/punkt")
except Exception:
    nltk.download("punkt")

from nltk.tokenize import sent_tokenize

def split_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    if not text:
        return []
    sentences = sent_tokenize(text)
    chunks: List[str] = []
    current_sentences: List[str] = []
    current_len = 0

    for sent in sentences:
        s = sent.strip()
        if not s:
            continue
        s_len = len(s) + 1  # account for a space or separator
        # If adding this sentence keeps us under or equal to target chunk_size, add it
        if current_len + s_len <= chunk_size or not current_sentences:
            current_sentences.append(s)
            current_len += s_len
        else:
            # finalize current chunk
            chunk_text = " ".join(current_sentences).strip()
            chunks.append(chunk_text)
            # Build overlap: start next chunk with tail sentences whose chars sum >= chunk_overlap
            overlap_sentences: List[str] = []
            overlap_chars = 0
            # iterate backwards through current_sentences to collect overlap
            for rev_sent in reversed(current_sentences):
                overlap_sentences.insert(0, rev_sent)  # building front to back
                overlap_chars += len(rev_sent) + 1
                if overlap_chars >= chunk_overlap:
                    break
            # start new current_sentences with overlap + current sentence
            current_sentences = overlap_sentences.copy()
            current_len = sum(len(x)+1 for x in current_sentences)
            # Now add the current sentence (that didn't fit) if it wasn't part of overlap
            # Note: if overlap already contains the sentence, avoid double-adding
            if current_sentences and current_sentences[-1] == s:
                # unlikely but safe
                pass
            else:
                current_sentences.append(s)
                current_len += s_len

    # flush last chunk
    if current_sentences:
        chunk_text = " ".join(current_sentences).strip()
        chunks.append(chunk_text)

    logger.info("split_into_chunks -> produced %d chunks (chunk_size=%d, overlap=%d)", len(chunks), chunk_size, chunk_overlap)
    return chunks
