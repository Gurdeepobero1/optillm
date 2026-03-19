from core.auth import get_user
from core.db import SessionLocal, Usage
from fastapi import FastAPI, Header
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
def ask(query: Query, x_api_key: str = Header(None)):
    start = time.time()

    user = get_user(x_api_key)
    if not user:
        return {"error": "Invalid API key"}

    cached = search_cache(query.prompt)

    if cached:
        latency = time.time() - start

        db = SessionLocal()
        db.add(Usage(
            user_id=user.id,
            query=query.prompt,
            latency=latency,
            cost=0,
            cached=True
        ))
        db.commit()
        db.close()

        return {
            "response": cached,
            "cached": True,
            "latency": latency
        }

    model = select_model(query.prompt)
    answer = query_llm(query.prompt)

    if "Error" not in answer:
        add_to_cache(query.prompt, answer)

    latency = time.time() - start

    db = SessionLocal()
    db.add(Usage(
        user_id=user.id,
        query=query.prompt,
        latency=latency,
        cost=0.001,
        cached=False
    ))
    db.commit()
    db.close()

    return {
        "response": answer,
        "model": model,
        "latency": latency,
        "cached": False
    }

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
    if "HTTP" not in answer and "Error" not in answer:
        add_to_cache(query.prompt, answer)

    latency = time.time() - start
    log(query.prompt, model, latency, False)

    return {
        "response": answer,
        "model": model,
        "cached": False,
        "latency": latency
    }