# setup.py
from setuptools import setup, find_packages

setup(
    name="medical_chatbot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "langchain==0.3.26",
        "langchain-openai==0.3.26",
        "langchain-community==0.3.26",
        "langchain-pinecone==0.2.0",
        "pinecone-client==5.0.0",
        "openai>=1.86.0,<2.0.0",
        "sentence-transformers==3.0.1",
        "pypdf==5.6.1",
        "pdfplumber==0.9.0",
        "python-dotenv==1.0.1",
        "pydantic==2.9.2"
    ],
)
