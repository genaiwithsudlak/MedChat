# data/scripts/preprocess_pdf.py

import os
import json
from pathlib import Path
from pypdf import PdfReader
import spacy
from spacy.matcher import PhraseMatcher
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ---------------------------------------------
# 1. LOAD LIGHTWEIGHT SPACY PIPELINE
# ---------------------------------------------
# spaCy blank model (super fast, no download needed)
nlp = spacy.blank("en")

# ---------------------------------------------
# 2. CUSTOM MEDICAL TERM MATCHER
# (You can keep extending this list)
# ---------------------------------------------
medical_terms = [
    "diabetes", "cancer", "asthma", "hypertension", "stroke",
    "heart attack", "arthritis", "depression", "anxiety",
    "bronchitis", "infection", "disease", "therapy",
    "treatment", "symptoms", "diagnosis", "prevention"
]

matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp.make_doc(term) for term in medical_terms]
matcher.add("MEDICAL_TERMS", patterns)

# ---------------------------------------------
# 3. READ PDF TEXT
# ---------------------------------------------
def load_pdf(pdf_path):
    print(f"[INFO] Reading PDF → {pdf_path}")
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


# ---------------------------------------------
# 4. CUSTOM TEXT PREPROCESSING
# ---------------------------------------------
def preprocess_text(text):
    doc = nlp(text)

    # capture matched medical entities
    matches = matcher(doc)
    extracted_terms = []

    for match_id, start, end in matches:
        span = doc[start:end]
        extracted_terms.append(span.text)

    cleaned = " ".join(text.split())  # normalize whitespace

    return cleaned, list(set(extracted_terms))  # unique


# ---------------------------------------------
# 5. CHUNKING FOR RAG
# ---------------------------------------------
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "?", "!"]
    )

    chunks = splitter.split_text(text)
    return chunks


# ---------------------------------------------
# 6. SAVE OUTPUT FILES
# ---------------------------------------------
def save_processed_data(chunks, entities, out_dir="data/processed"):
    os.makedirs(out_dir, exist_ok=True)

    entries_path = os.path.join(out_dir, "entries.json")
    entities_path = os.path.join(out_dir, "medical_terms.json")

    with open(entries_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)

    with open(entities_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=4)

    print(f"[OK] Saved chunks → {entries_path}")
    print(f"[OK] Saved extracted medical terms → {entities_path}")


# ---------------------------------------------
# 7. MAIN
# ---------------------------------------------
if __name__ == "__main__":
    pdf_path = Path("data/raw/gale_encyclopedia_vol2.pdf")

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    raw_text = load_pdf(pdf_path)
    cleaned_text, extracted_entities = preprocess_text(raw_text)
    chunks = chunk_text(cleaned_text)

    save_processed_data(chunks, extracted_entities)
    print("[DONE] Preprocessing completed successfully.")
