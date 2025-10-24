from pathlib import Path
import csv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Paths
BASE_DIR = Path(__file__).resolve().parent
data_path = BASE_DIR / "data" / "qa.csv"
store_dir = BASE_DIR / "vectorstore"
store_dir.mkdir(parents=True, exist_ok=True)

def main():
    docs, metas = [], []

    with data_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # normalize headers to lowercase and strip values
            fields = { (k or "").strip().lower(): (v or "").strip()
                       for k, v in row.items() }

            q = fields.get("question") or fields.get("questions")
            a = fields.get("answer")   or fields.get("answers")

            if q and a:
                docs.append(f"Q: {q}\n\nA: {a}")
                metas.append({"question": q})

    if not docs:
        raise RuntimeError(
            f"No rows built from {data_path}. "
            f"Expected columns like 'question/answer' "
            f"(any case). Found headers: {getattr(reader, 'fieldnames', None)}"
        )

    embed = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )
    db = FAISS.from_texts(docs, embed, metadatas=metas)
    db.save_local(str(store_dir))
    print("✅ Vectorstore built and saved at:", store_dir)

if __name__ == "__main__":
    main()


