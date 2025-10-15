from __future__ import annotations
import os, csv
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def read_qa_csv(path: str) -> List[Document]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {os.path.abspath(path)}")
    with open(path, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError("CSV is empty.")
    header = [h.strip() for h in rows[0]]
    lower = [h.lower() for h in header]
    def idx(names):
        for n in names:
            if n in lower:
                return lower.index(n)
        return None
    q_i = idx(["question","questions","q","prompt"])
    a_i = idx(["answer","answers","a","response","reply"])
    if q_i is None: q_i = 0
    if a_i is None: a_i = 1 if len(header) > 1 else 0
    docs: List[Document] = []
    for i, row in enumerate(rows[1:]):
        q = row[q_i].strip() if len(row) > q_i else ""
        a = row[a_i].strip() if len(row) > a_i else ""
        if not q and not a: 
            continue
        text = f"Q: {q}\n\nA: {a}"
        meta = {"source": os.path.basename(path), "row": i+1, "question": q}
        docs.append(Document(page_content=text, metadata=meta))
    if not docs:
        raise ValueError("No valid rows found in the CSV.")
    return docs

def ingest_csv_to_faiss(csv_path: str, store_dir: str = "vectorstore") -> str:
    print(f"Ingesting {csv_path} -> {store_dir} ...")
    docs = read_qa_csv(csv_path)
    print(f"Using local embeddings: {MODEL_NAME}")
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vs = FAISS.from_documents(docs, embeddings)
    os.makedirs(store_dir, exist_ok=True)
    vs.save_local(store_dir)
    print("Ingestion complete. Vectorstore saved to:", os.path.abspath(store_dir))
    return store_dir

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Ingest a Q/A CSV into a FAISS vectorstore.")
    p.add_argument("csv", help="Path to CSV (UTF-8).")
    p.add_argument("--store", default="vectorstore", help="Directory to save the FAISS store.")
    args = p.parse_args()
    ingest_csv_to_faiss(args.csv, args.store)

