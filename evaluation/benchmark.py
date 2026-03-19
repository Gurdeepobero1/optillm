import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
from core.llm import query_llm
from core.cache import search_cache, add_to_cache, clear_cache

queries = [
    "What is AI?",
    "Explain machine learning",
    "What is AI?",  # repeated (cache hit)
]

def run_benchmark():
    clear_cache()

    print("\n--- FIRST PASS (NO CACHE) ---")
    start = time.time()

    for q in queries:
        res = query_llm(q)
        add_to_cache(q, res)

    time_no_cache = time.time() - start

    print("\n--- SECOND PASS (WITH CACHE) ---")
    start = time.time()

    for q in queries:
        cached = search_cache(q)
        if cached:
            res = cached
        else:
            res = query_llm(q)

    time_with_cache = time.time() - start

    print("\n--- RESULTS ---")
    print("Time without cache:", round(time_no_cache, 2))
    print("Time with cache:", round(time_with_cache, 2))

    improvement = ((time_no_cache - time_with_cache) / time_no_cache) * 100
    print(f"Latency Improvement: {round(improvement, 2)}%")

if __name__ == "__main__":
    run_benchmark()