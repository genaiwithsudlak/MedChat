# filename: scripts/validate_env.py
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

required = ["OPENAI_API_KEY", "PINECONE_API_KEY", "PINECONE_ENV", "PINECONE_INDEX"]
missing = [k for k in required if not os.getenv(k)]
print("Missing env vars:" if missing else "All required env vars present.")
pprint(missing)
