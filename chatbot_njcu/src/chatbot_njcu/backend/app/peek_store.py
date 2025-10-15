from __future__ import annotations
import os
from collections import Counter

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
STORE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vectorstore"))

print("Vectorstore dir:", STORE_DIR)
faiss_path = os.path.join(STORE_DIR, "index.faiss")
if not os.path.exists(faiss_path):
    print("! No FAISS index found at:", faiss_path)
    raise SystemExit(1)

# embeddings object is required to load FAISS
emb = HuggingFaceEmbeddings(model_name=MODEL_NAME)
vs = FAISS.load_local(STORE_DIR, emb, allow_dangerous_deserialization=True)

docs = list(vs.docstore._dict.values())
print("Documents in index:", len(docs))

# Which files were used to build this index?
sources = Counter(d.metadata.get("source", "(none)") for d in docs)
print("Source files and counts:", dict(sources))

# Show row range and a few examples
rows = [d.metadata.get("row") for d in docs if "row" in d.metadata]
if rows:
    print("Row range:", min(rows), "to", max(rows))

print("\nSample docs:")
for d in docs[:3]:
    print("-", d.metadata)
    print("  ", d.page_content[:160].replace("\n", " "), "…")
