from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import csv, os

# Paths
data_path = "src/chatbot_njcu/backend/data/qa.csv"
store_dir = "src/chatbot_njcu/backend/vectorstore"

# Load Q&A data
docs, metas = [], []
with open(data_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        q, a = row["question"], row["answer"]
        docs.append(f"Q: {q}\n\nA: {a}")
        metas.append({"question": q})

# Build embeddings
embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS index
db = FAISS.from_texts(docs, embed, metadatas=metas)
db.save_local(store_dir)

print("✅ Vectorstore built and saved at:", store_dir)
