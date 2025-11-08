def filter_results(results, query=None, threshold=0.2, top_k=5):
    hits = results.get("hits", {}).get("hits", [])
    if not hits:
        return []

    # безопасно ищем максимальный score
    max_score = 0.0
    for h in hits:
        try:
            s = float(h.get("_score", 0))
            if s > max_score:
                max_score = s
        except (ValueError, TypeError):
            continue

    filtered = []
    query_tokens = query.lower().split() if query else []

    for h in hits:
        try:
            score = float(h.get("_score", 0))
        except (ValueError, TypeError):
            continue

        if score < max_score * threshold:
            continue

        if query_tokens:
            # объединяем текст всех ключевых полей
            field_values = " ".join([h["_source"].get(f, "").lower()
                                     for f in ["name","brand","category","keywords"]])
            # частичное совпадение хотя бы одного токена
            if not any(tok in field_values for tok in query_tokens):
                continue

        filtered.append(h)
        if len(filtered) >= top_k:
            break

    return filtered
