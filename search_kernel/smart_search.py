from search_kernel.corrections import fix_layout_bidirectional
from search_kernel.search import search
from search_kernel.filter import filter_results

def smart_search(user_input, threshold=0.3):
    results = search(user_input)
    top = filter_results(results, user_input, threshold)
    if top:
        return top

    converted1, converted2 = fix_layout_bidirectional(user_input)

    #если ничего не найдено — пробуем перевернуть раскладку
    results = search(converted1)
    top = filter_results(results, converted1, threshold)
    if top:
        return top

    results = search(converted2)
    top = filter_results(results, converted2, threshold)

    return top
