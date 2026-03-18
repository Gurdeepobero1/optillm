import faiss
import numpy as np
from core.embed import get_embedding

dim = 384
index = faiss.IndexFlatL2(dim)
stored_data = []

def search_cache(query):
    if index.ntotal == 0:
        return None

    emb = np.array([get_embedding(query)]).astype("float32")
    D, I = index.search(emb, 1)

    if D[0][0] < 0.3:
        return stored_data[I[0][0]][1]

    return None

def add_to_cache(query, response):
    emb = np.array([get_embedding(query)]).astype("float32")
    index.add(emb)
    stored_data.append((query, response))
    