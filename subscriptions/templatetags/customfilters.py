from django import template

from AllNews.models import CATEGORY_CATEGORIES


register = template.Library()


@register.filter()
def get_fullname(text: str):
    for item in CATEGORY_CATEGORIES:
        if item[0] == text:
            return item[1]
