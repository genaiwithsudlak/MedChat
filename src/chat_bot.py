# File: src/chat_bot.py

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
import os

def main():
    print("🔍 Loading FAISS index...")

    index_path = "data/index/medical_book"   # no .index extension
    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(search_kwargs={"k": 5})

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    print("✅ Chatbot is ready! Ask medical questions.\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit", "bye"]:
            print("Goodbye! 👋")
            break

        result = qa.invoke({"query": query})
        print("\nBot:", result["result"])
        print("-" * 60)

if __name__ == "__main__":
    main()
