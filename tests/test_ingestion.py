# tests/test_ingestion.py
from src.ingestion.text_cleaning import clean_text

def test_clean_text_basic():
    s = "Hello \r\n\r\n World \t\t!"
    cleaned = clean_text(s)
    assert "World" in cleaned
    assert "\t" not in cleaned
