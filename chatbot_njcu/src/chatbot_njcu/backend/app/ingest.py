from typing import List
import csv
import os

from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def read_qa_csv(path: str) -> List[Document]:
    """
    Read a CSV file with headers 'question' and 'answer' and return Documents.
    Each Document.text contains question + two newlines + answer.
    """
    docs = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            q = row.get('question', '').strip()
            a = row.get('answer', '').strip()
            if not q and not a:
                continue
            text = f"Q: {q}\n\nA: {a}"
            metadata = {"source": os.path.basename(path), "row": i, "question": q}
            docs.append(Document(page_content=text, metadata=metadata))
    return docs

def ingest_csv_to_faiss(csv_path: str, store_dir: str = "vectorstore"):
    """
    Ingest CSV into a FAISS vectorstore persisted at store_dir.
    """
    print(f"Ingesting {csv_path} -> {store_dir} ...")
    docs = read_qa_csv(csv_path)
    if not docs:
        raise ValueError("No documents found in the CSV file.")

    # Create embeddings (requires OPENAI_API_KEY in env)
    embeddings = OpenAIEmbeddings()

    # Build FAISS index and persist
    vectorstore = FAISS.from_documents(docs, embeddings)
    # Create dir if missing
    os.makedirs(store_dir, exist_ok=True)
    vectorstore.save_local(store_dir)
    print("Ingestion complete. Vectorstore saved to:", store_dir)
    return store_dir

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("csv", help="Path to CSV with question,answer columns")
    p.add_argument("--store", default="vectorstore", help="Directory to save the FAISS store")
    args = p.parse_args()
    ingest_csv_to_faiss(args.csv, args.store)