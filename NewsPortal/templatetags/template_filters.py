from django import template


register = template.Library()


@register.filter()
def censure(text: str):
    if type(text) is not str:
        raise Exception('Фильтр применён не к строковой переменной!')

    words = text.split(' ')
    for index, word in enumerate(words):
        if word.startswith('редиск'): # редиска\редиски\редиску
            words[index] = 'р******'

    return ' '.join(words)
