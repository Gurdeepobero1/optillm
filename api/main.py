from fastapi import FastAPI
from pydantic import BaseModel
import time
from dotenv import load_dotenv

from core.router import select_model
from core.cache import search_cache, add_to_cache
from core.llm import query_llm
from core.metrics import log

load_dotenv()

app = FastAPI()

class Query(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "OptiLLM running 🚀"}

@app.post("/ask")
def ask(query: Query):
    start = time.time()

    # Check cache
    cached = search_cache(query.prompt)
    if cached:
        latency = time.time() - start
        log(query.prompt, "cache", latency, True)
        return {
            "response": cached,
            "cached": True,
            "latency": latency
        }

    # Select model
    model = select_model(query.prompt)

    # Get response
    answer = query_llm(query.prompt)

    # Store in cache
    add_to_cache(query.prompt, answer)

    latency = time.time() - start
    log(query.prompt, model, latency, False)

    return {
        "response": answer,
        "model": model,
        "cached": False,
        "latency": latency
    }