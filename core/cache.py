cache_store = {}

def search_cache(query):
    return cache_store.get(query)

def add_to_cache(query, response):
    cache_store[query] = response

def clear_cache():
    global cache_store
    cache_store = {}