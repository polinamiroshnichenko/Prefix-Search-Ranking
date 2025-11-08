import requests
def search(query, es_url="http://localhost:9200", index_name="products"):
    payload = {
        "query": {
            "bool": {
                "should": [
                    {"multi_match": {
                        "query": query,
                        "fields": [
                            "name^4",
                            "name.ngram^2",
                            "name.sasy^3",
                            "brand.ngram^2",
                            "category.ngram^2",
                            "keywords.ngram^4",
                            "description^2",

                        ],
                        "type": "bool_prefix"
                    }}
                ]
            }
        }
    }
    r = requests.post(f"{es_url}/{index_name}/_search", json=payload)
    return r.json()
