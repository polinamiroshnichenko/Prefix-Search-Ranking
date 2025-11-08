def filter_results(results, query, threshold=0.2):
    hits = results["hits"]["hits"]
    if not hits:
        return []

    max_score = hits[0]["_score"]
    filtered = [
        h for h in hits
        if h["_score"] > max_score * threshold
        and (query.lower() in h["_source"].get("brand_ngram", "").lower()
             or query.lower() in h["_source"].get("category_ngram", "").lower()
             or query.lower() in h["_source"].get("name", "").lower())
    ]
    return filtered[:5]
