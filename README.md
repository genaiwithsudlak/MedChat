# filename: README.md

Medical Chatbot (RAG + LangChain + Pinecone + Streamlit)

## Quickstart (local)

1. Create & activate venv
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate      # windows
   source .venv/bin/activate     # mac/linux
Install deps

bash
Copy code
pip install -r requirements.txt
python -m pip install -e .
Create .env from .env.example and set API keys.

Preprocess PDF and upload embeddings:

bash
Copy code
python -c "from src.ingestion.preprocess_pdf import run_preprocessing; run_preprocessing('data/raw/gale_encyclopedia_vol2.pdf')"
Run backend:

bash
Copy code
uvicorn src.api.app:app --reload --port 8000
Run UI:

bash
Copy code
streamlit run src.ui.streamlit_app.py
Notes
Replace model choices in src/llm/openai_llm.py with models you have access to.

Configure Pinecone index dimension to match embedding model in pinecone_init.py.

yaml
Copy code

---

## 22) Tests (basic placeholders) — `tests/test_ingestion.py`, etc.
(I included stubs in the scaffolding earlier — keep them; you can expand to realistic unit tests.)

---

## Run checklist & tips

1. Create a fresh virtual env, activate it.
2. `pip install -r requirements.txt`
   - If scispaCy model `en-core-sci-lg` is needed, install with:
     ```bash
     pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/en_core_sci_lg-0.5.1.tar.gz
     ```
3. `python -m pip install -e .`
4. Set `.env` with real keys. `USE_OPENAI_EMBEDDINGS=true` if you want OpenAI embeddings; set `OPENAI_API_KEY`.
5. Update `src/llm/openai_llm.py` model selection to a model you have access to (e.g., `"gpt-4o-mini"`, `"gpt-4o"`, `"gpt-4"` etc.) or swap in LangChain LLM wrapper.
6. Run preprocessing to populate Pinecone and `data/processed/chunks_metadata.json`.
7. Start backend & UI.

---

## Final notes / caveats

- I provided working, end-to-end code for the main pipeline. Some parts are intentionally conservative / placeholder (LLM model name, model drift monitoring, dimension autodetection) and must be tailored to your environment and available models.
- Pinecone index dimension must match your embedding vector length. Default in code is 384 (MiniLM). If you use OpenAI embeddings (`text-embedding-3-small`), that's 1536; update `pinecone_init.py` accordingly before creating the index.
- For production grade: add authentication to API, rate limiting, logging to ELK/CloudWatch, more extensive tests, and human-in-the-loop moderation for high-risk answers — we can add those iteratively.

---

If you want, I will now:
1. Generate these files into a zip and provide a download link (I cannot write files to your machine directly but I can output everything so you can paste), **or**
2. Create specific modules first (e.g., fully implemented LangChain RAG chain using LangChain APIs), or
3. Help you run the first pipeline step (`preprocess_pdf.run_preprocessing`) locally and troubleshoot environment errors.

Which next action do you want me to take?