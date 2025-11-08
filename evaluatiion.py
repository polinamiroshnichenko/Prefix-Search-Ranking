import csv
import time
from search_kernel.smart_search import smart_search

TOP_K = 5
QUERIES_FILE = "/Users/polina/PycharmProjects/Prefix-Search-Ranking/data/prefix_queries.csv"
OUTPUT_FILE = "/Users/polina/PycharmProjects/Prefix-Search-Ranking/data/evaluation.csv"

results_list = []

with open(QUERIES_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        query = row["query"]

        start_time = time.time()
        top_results = smart_search(query)[:TOP_K]
        latency_ms = (time.time() - start_time) * 1000

        explanations = []
        for r in top_results:
            explanation = []
            source = r["_source"]
            if query.lower() in source.get("name", "").lower():
                explanation.append("name match")
            if query.lower() in source.get("brand", "").lower():
                explanation.append("brand match")
            if query.lower() in source.get("category", "").lower():
                explanation.append("category match")
            explanations.append(", ".join(explanation))

        row_dict = {
            "query": query,
            "latency_ms": round(latency_ms, 1),
        }

        for i in range(TOP_K):
            row_dict[f"top_{i+1}"] = top_results[i]["_id"] if i < len(top_results) else ""
            row_dict[f"top_{i+1}_score"] = top_results[i]["_score"] if i < len(top_results) else ""
            row_dict[f"top_{i+1}_category"] = top_results[i]["_source"].get("category", "") if i < len(top_results) else ""
            row_dict[f"top_{i+1}_reason"] = explanations[i] if i < len(explanations) else ""

        results_list.append(row_dict)

fieldnames = ["query", "latency_ms"]
for i in range(TOP_K):
    fieldnames += [f"top_{i+1}", f"top_{i+1}_score", f"top_{i+1}_category", f"top_{i+1}_reason"]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results_list)

print(f"saved to {OUTPUT_FILE}")

#precision
precision_hits = 0
for r in results_list:
    for i in range(3):
        if r[f"top_{i+1}"]:
            precision_hits += 1
            break
precision_at_3 = precision_hits / len(results_list)
print(f"Precision@3: {precision_at_3:.2f}")
