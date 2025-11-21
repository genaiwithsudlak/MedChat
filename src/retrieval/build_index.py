# File: src/retrieval/build_index.py

import os
import json
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

# CONFIG
DATA_DIR = Path("data/processed/Medical_book")
INDEX_DIR = Path("data/index")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

def load_entries(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Check for content key
    if isinstance(data, list):
        if "content" in data[0]:
            return data
        else:
            raise ValueError("entries.json must contain 'content' key for each entry.")
    elif isinstance(data, dict):
        if "text" in data:
            return [{"content": data["text"], "source": data.get("source", "")}]
        elif "content" in data:
            return [{"content": data["content"], "source": data.get("source", "")}]
        else:
            raise ValueError("Unexpected format. Must contain 'text' or 'content'.")
    else:
        raise ValueError("Unsupported JSON structure.")

def chunk_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return splitter.split_text(text)

def main():
    print("📥 Loading ingestion output for: Medical_book")
    entries_file = DATA_DIR / "entries.json"
    entries = load_entries(entries_file)

    print(f"📄 Processing {len(entries)} entries...")
    all_chunks = []
    for entry in entries:
        text = entry["content"]
        chunks = chunk_text(text)
        for c in chunks:
            all_chunks.append({"text": c, "source": entry.get("source", "")})

    print(f"🔹 Total chunks created: {len(all_chunks)}")

    # Embeddings
    embeddings = OpenAIEmbeddings()
    texts = [c["text"] for c in all_chunks]
    metadatas = [{"source": c["source"]} for c in all_chunks]

    print("💾 Building FAISS index...")
    db = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_path = INDEX_DIR / "medical_book.index"
    db.save_local(str(index_path))
    print(f"✅ Index saved at {index_path}")

if __name__ == "__main__":
    main()
