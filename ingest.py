import pandas as pd
import numpy as np
import faiss
import requests

# Load your Excel FAQ file
df = pd.read_excel("cleaned_faqs.xlsx")

# Pick the model we’ll use for embeddings
EMBED_MODEL = "nomic-embed-text"

# Function to get embeddings from Ollama
def embed(text):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    r.raise_for_status()
    v = np.array(r.json()["embedding"], dtype="float32")
    return v

# Generate embeddings for all questions
texts = df["question"].tolist()
vecs = np.vstack([embed(t) for t in texts])

# Create a FAISS index (vector database in memory)
index = faiss.IndexFlatL2(vecs.shape[1])
index.add(vecs)

# Save index + dataframe for later use
faiss.write_index(index, "faiss.index")
df.to_pickle("faqs.pkl")

print("✅ Finished building the knowledge base!")

