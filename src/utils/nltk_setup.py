import nltk

def ensure_nltk():
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
