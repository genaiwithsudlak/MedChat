# File: app/components/chat_ui.py

import streamlit as st
from pathlib import Path
import sys

# Add project root to sys.path so we can import src modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.utils.logger import get_logger  # Absolute import works

# ----- NEW LANGCHAIN IMPORTS -----
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage

logger = get_logger(__name__)

# ----- CONFIG -----
INDEX_PATH = Path("data/index/medical_book")
EMBEDDINGS = OpenAIEmbeddings()
DB = FAISS.load_local(INDEX_PATH, EMBEDDINGS, allow_dangerous_deserialization=True)
RETRIEVER = DB.as_retriever(search_kwargs={"k": 5})

LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
QA_CHAIN = RetrievalQA.from_chain_type(llm=LLM, retriever=RETRIEVER, return_source_documents=True)

OPINION_LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# ----- SESSION STATE -----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🩺 Medical Chatbot")

query = st.text_input("Ask a medical question:")

# ----- FUNCTIONS -----
def get_opinion(question: str) -> str:
    """Fetch general opinion from OpenAI."""
    try:
        response = OPINION_LLM.invoke([HumanMessage(content=f"Provide your general opinion on: {question}")])
        return response.content
    except Exception as e:
        logger.error(f"Error in OpenAI Opinion: {e}")
        return "Error fetching opinion."

# ----- PROCESS QUERY -----
if query:
    try:
        result = QA_CHAIN.invoke({"query": query})
        answer = result["result"]
        st.session_state.chat_history.append({"user": query, "bot": answer})
    except Exception as e:
        logger.error(f"Error in QA_CHAIN: {e}")
        st.session_state.chat_history.append({"user": query, "bot": "Error fetching answer."})

# ----- DISPLAY CHAT -----
for idx, chat in enumerate(reversed(st.session_state.chat_history)):
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
    
    # OpenAI Opinion button with unique key
    if st.button("OpenAI Opinion", key=f"opinion_{len(st.session_state.chat_history) - idx}_{chat['user']}"):
        opinion_text = get_opinion(chat['user'])
        st.markdown(f"**OpenAI Opinion:** {opinion_text}")
