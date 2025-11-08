import requests
import json

es_url = "http://localhost:9200"
index_name = "products"

mapping = {
    "settings": {
        "analysis": {
            "analyzer": {
                "edge_ngram_analyzer": {
                    "tokenizer": "edge_ngram_tokenizer",
                    "filter": ["lowercase"]
                }
            },
            "tokenizer": {
                "edge_ngram_tokenizer": {
                    "type": "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 15,
                    "token_chars": ["letter", "digit"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "fields": {
                    "ngram": {"type": "text", "analyzer": "edge_ngram_analyzer"},
                    "sasy": {"type": "search_as_you_type"}
                }
            },
            "brand": {
                "type": "text",
                "fields": {
                    "ngram": {"type": "text", "analyzer": "edge_ngram_analyzer"},
                    "keyword": {"type": "keyword"}
                }
            },
            "category": {
                "type": "text",
                "fields": {
                    "ngram": {"type": "text", "analyzer": "edge_ngram_analyzer"},
                    "keyword": {"type": "keyword"}
                }
            },
            "keywords": {
                "type": "text",
                "fields": {
                    "ngram": {"type": "text", "analyzer": "edge_ngram_analyzer"},
                    "keyword": {"type": "keyword"}
                }
            },
            "description": {"type": "text"},
            "weight": {"type": "float"},
            "package_size": {"type": "long"},
            "price": {"type": "float"},
            "image_url": {"type": "text"}
        }
    }
}

resp = requests.put(f"{es_url}/{index_name}", json=mapping)

