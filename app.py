# app.py — minimal chatbot API (Ollama + your FAQ index)
from fastapi import FastAPI
from pydantic import BaseModel
import faiss, numpy as np, pandas as pd, requests, json

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "llama3.2:3b"       # small model that fits your RAM
TOP_K = 5

# load index + FAQ data
index = faiss.read_index("faiss.index")
df = pd.read_pickle("faqs.pkl")   # contains your columns (question, answer, etc.)

app = FastAPI()

@app.get("/ping")
def ping():
    return {"pong": True}


def embed(text: str) -> np.ndarray:
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype="float32").reshape(1, -1)
    # normalize for cosine-like scoring with L2 index
    faiss.normalize_L2(v)
    return v

def ask_llm(context: str, question: str) -> str:
    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {"role": "system", "content":
             "You are a university Career & Professional Development bot. "
             "Answer ONLY using the provided CONTEXT. If the info is missing, "
             "say you don't know and offer to connect the student to the office. "
             "Keep answers to 2–5 sentences."},
            {"role": "user", "content":
             f"[CONTEXT]\n{context}\n\n[QUESTION]\n{question}\n\nUse only the CONTEXT above."}
        ],
        "stream": False
    }
    r = requests.post("http://localhost:11434/api/chat", json=payload)
    r.raise_for_status()
    return r.json()["message"]["content"]

class QIn(BaseModel):
    question: str

@app.post("/chat")
def chat(body: QIn):
    qvec = embed(body.question)
    D, I = index.search(qvec, TOP_K)

    # build short context from nearest FAQs
    rows = df.iloc[I[0]][["question", "answer"]].fillna("")
    context = "\n\n".join([f"Q: {r.question}\nA: {r.answer}" for r in rows.itertuples()])

    answer = ask_llm(context, body.question)
    return {"answer": answer}
