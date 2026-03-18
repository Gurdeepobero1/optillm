def select_model(query: str):
    q = query.lower()

    if len(query.split()) < 20:
        return "fast-model"
    elif "analyze" in q or "strategy" in q or "compare" in q:
        return "smart-model"
    else:
        return "balanced-model"