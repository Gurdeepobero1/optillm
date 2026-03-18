logs = []

def estimate_cost(prompt, model):
    tokens = len(prompt.split())

    # fake pricing (for demo)
    if model == "fast-model":
        cost = tokens * 0.0001
    elif model == "smart-model":
        cost = tokens * 0.0005
    else:
        cost = tokens * 0.0003

    return round(cost, 6)

def log(query, model, latency, cached):
    cost = 0 if cached else estimate_cost(query, model)

    logs.append({
        "query": query,
        "model": model,
        "latency": round(latency, 3),
        "cached": cached,
        "cost": cost
    })