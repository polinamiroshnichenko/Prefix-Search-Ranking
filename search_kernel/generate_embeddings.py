import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

from sentence_transformers import SentenceTransformer
import requests

es_url = "http://localhost:9200"
index_name = "products"

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

r = requests.get(f"{es_url}/{index_name}/_search", json={"size": 1000, "query": {"match_all": {}}})
products = r.json().get("hits", {}).get("hits", [])

for p in products:
    product_id = p["_id"]
    source = p["_source"]

    name = source.get("name", "")
    description = source.get("description", "")
    keywords = source.get("keywords", "")
    brand = source.get("brand", "")

    text = f"{name} {description} {keywords} {brand}"
    vector = model.encode(text).tolist()

    payload = {"doc": {"embedding": vector}}
    requests.post(f"{es_url}/{index_name}/_update/{product_id}", json=payload)

print("Embeddings добавлены для всех товаров (name + description + keywords + brand)")
