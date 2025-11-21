# src/ui/streamlit_app.py
from src.utils.logger import logger
import streamlit as st
from src.api.routes import init_routes  # example

def create_app():
    logger.info("Building streamlit UI")
    st.set_page_config(page_title="Medical Chatbot")
    st.title("Medical Chatbot")
    # import chat UI
    from app.components.chat_ui import render_chat
    render_chat()
