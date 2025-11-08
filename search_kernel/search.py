import requests
def search(query, es_url="http://localhost:9200", index_name="products"):
    payload = {
        "query": {
            "bool": {
                "should": [
                    {"multi_match": {
                        "query": query,
                        "fields": [
                            "name^3",
                            "name.ngram^2",
                            "name.sasy^2",
                            "brand^1.5",
                            "category^1.5",
                            "description"
                        ],
                        "type": "bool_prefix"
                    }}
                ]
            }
        }
    }
    r = requests.post(f"{es_url}/{index_name}/_search", json=payload)
    return r.json()
