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

import requests

def search_by_embedding(vector, es_url="http://localhost:9200", index_name="products", top_k=5):
    payload = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": vector}
                }
            }
        }
    }
    r = requests.post(f"{es_url}/{index_name}/_search", json=payload)
    return r.json()


