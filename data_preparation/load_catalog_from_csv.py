import pandas as pd
import requests
import json

def load_csv_to_elasticsearch(csv_file, es_url, index_name):
    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        doc = row.to_dict()
        doc_id = doc.pop('id')

        resp = requests.put(f"{es_url}/{index_name}/_doc/{doc_id}", json=doc)
        if resp.status_code != 201 and resp.status_code != 200:
            print(f"Error {doc_id}: {resp.text}")

    print("done")

load_csv_to_elasticsearch('/Users/polina/PycharmProjects/Prefix-Search-Ranking/data/catalog_products.csv', 'http://localhost:9200', 'products')

