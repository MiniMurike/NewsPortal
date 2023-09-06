from django import template
from AllNews.models import CATEGORY_TYPES, CATEGORY_CATEGORIES, Category


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


@register.filter()
def get_fulltype(text):
    for item in CATEGORY_TYPES:
        if item[0] == text:
            return item[1]


@register.filter()
def get_fullcategories(post):
    qs = Category.objects.filter(
        postcategory__post__id=post.id
    )

    result = []
    for item in qs:
        result.append(str(item))

    result = ', '.join(result)

    return result
