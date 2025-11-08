def fix_layout_bidirectional(text):
    layout_map_ru_to_en = str.maketrans(
        "йцукенгшщзхъфывапролджэячсмитьбю",
        "qwertyuiop[]asdfghjkl;'zxcvbnm,."
    )
    layout_map_en_to_ru = str.maketrans(
        "qwertyuiop[]asdfghjkl;'zxcvbnm,.",
        "йцукенгшщзхъфывапролджэячсмитьбю"
    )

    # латиница - кириллица
    converted1 = text.translate(layout_map_en_to_ru)
    # кириллица - латиница
    converted2 = text.translate(layout_map_ru_to_en)

    return converted1, converted2
