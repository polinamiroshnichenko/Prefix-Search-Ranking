import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'


from search_kernel.corrections import fix_layout_bidirectional
from search_kernel.search import search, search_by_embedding
from search_kernel.filter import filter_results
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

def smart_search(user_input, threshold=0.3, top_k=5):
    # 1. Текстовый поиск
    results = search(user_input)
    top = filter_results(results, user_input, threshold)
    if top:
        return top

    # 2. Перевернутые раскладки
    converted1, converted2 = fix_layout_bidirectional(user_input)
    for q in [converted1, converted2]:
        results = search(q)
        top = filter_results(results, q, threshold)
        if top:
            return top

    # 3. Семантический поиск по embedding
    vector = model.encode(user_input).tolist()
    emb_results = search_by_embedding(vector, top_k=top_k)
    top = filter_results(emb_results, threshold=0)
    return top
