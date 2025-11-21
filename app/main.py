# app/main.py
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.ui.streamlit_app import create_app
from src.utils.logger import logger

if __name__ == "__main__":
    logger.info("Launching Streamlit app")
    create_app()
