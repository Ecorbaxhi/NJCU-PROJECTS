from __future__ import annotations

import os, re, csv
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# -------------------- Config --------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
STORE_DIR = os.getenv(
    "STORE_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vectorstore"))
)
PUBLIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))

app = FastAPI(title="NJCU Chatbot API")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://njcu-projects.onrender.com",  # your Render backend origin
        "https://ecorbaxhi.github.io",          # your GitHub Pages (if it calls the API)
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Static frontend --------------------
app.mount("/static", StaticFiles(directory=PUBLIC_DIR), name="static")

@app.get("/")
def home():
    return RedirectResponse(url="/static/chat.html")

# -------------------- Models --------------------
class QueryRequest(BaseModel):
    question: str
    k: int | None = 3

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict] = []

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    helpful: bool
    version: str | None = None

# -------------------- Lazy singletons --------------------
_embeddings = None
_vs = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_NAME,
            model_kwargs={"device": "cpu"}  # keep CPU to avoid meta-tensor issue
        )
    return _embeddings

def get_db():
    global _vs
    if _vs is None:
        _vs = FAISS.load_local(
            STORE_DIR,
            get_embeddings(),
            allow_dangerous_deserialization=True,
        )
    return _vs

# -------------------- Health --------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------- Version helpers --------------------
def _find_csv_path() -> Path:
    """Walk up from this file until we find data/qa.csv."""
    here = Path(__file__).resolve()
    for up in range(1, 8):
        candidate = here.parents[up-1] / "data" / "qa.csv"
        if candidate.exists():
            return candidate
    return (here.parent.parent.parent.parent / "data" / "qa.csv")

DATA_CSV = _find_csv_path()
DATA_DIR = DATA_CSV.parent
FEEDBACK_CSV = DATA_DIR / "feedback.csv"

def _read_version_from_csv(path: Path) -> str:
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        if len(rows) >= 2 and len(rows[1]) >= 2:
            return (rows[1][1] or "").strip() or "(unknown)"
    except Exception:
        pass
    return "(unknown)"

@app.get("/version")
def version():
    try:
        vs = get_db()
        count = len(vs.index_to_docstore_id)
    except Exception:
        count = None
    return {
        "status": "ok",
        "csv_path": str(DATA_CSV),
        "version": _read_version_from_csv(DATA_CSV),
        "docs": count,
    }

@app.post("/reload")
def reload_index():
    """Drop the in-memory FAISS so next query reloads from disk."""
    global _vs
    _vs = None
    return {"status": "reloaded"}

# -------------------- Feedback helpers --------------------
def _append_feedback(row: dict):
    FEEDBACK_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = FEEDBACK_CSV.exists()
    with FEEDBACK_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "timestamp", "helpful", "question", "answer", "version", "client"
        ])
        if not file_exists:
            w.writeheader()
        w.writerow(row)

@app.post("/feedback")
async def feedback(req: Request, body: FeedbackRequest):
    client = req.client.host if req.client else "unknown"
    _append_feedback({
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "helpful": "yes" if body.helpful else "no",
        "question": (body.question or "").strip(),
        "answer": (body.answer or "").strip(),
        "version": body.version or "",
        "client": client,
    })
    return {"status": "ok"}

# -------------------- Query --------------------
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s or "")).strip().lower()

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    vs = get_db()
    k = max(1, (req.k or 3))


    # --- Special intent: respond to "thank you" or similar ---
    gratitude = ["thank you", "thanks", "thx", "thank u"]
    q_lower = req.question.strip().lower()
    if any(word in q_lower for word in gratitude):
        return QueryResponse(
            answer="You're very welcome! Always happy to assist 😊",
            sources=[]
        )



    # 1) try exact (normalized) question match from a larger candidate pool
    try:
        candidates = vs.similarity_search_with_score(req.question, k=max(10, k))
    except Exception:
        candidates = [(d, None) for d in vs.similarity_search(req.question, k=max(10, k))]

    qn = _norm(req.question)
    for doc, _ in candidates:
        if _norm(doc.metadata.get("question", "")) == qn:
            ans = doc.page_content.split("\n\nA:", 1)[-1].strip()
            return QueryResponse(
                answer=ans,
                sources=[{"text": doc.page_content, "metadata": doc.metadata}],
            )

    # 2) fall back to normal semantic retrieval (simpler & version-proof)
    docs = vs.similarity_search(req.question, k=k)

    if not docs:
        return QueryResponse(
            answer="Sorry — I couldn’t find that in the knowledge base.",
            sources=[]
        )

    best = docs[0]
    ans = best.page_content.split("\n\nA:", 1)[-1].strip()
    return QueryResponse(
        answer=ans,
        sources=[{"text": d.page_content, "metadata": d.metadata} for d in docs],
    )


