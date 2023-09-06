from django_filters import (
    FilterSet, DateTimeFilter, ModelMultipleChoiceFilter, ModelChoiceFilter, ChoiceFilter, CharFilter)

from .models import Post, Author, CATEGORY_TYPES, Category
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        )
    )
    type = ChoiceFilter(
        choices=CATEGORY_TYPES,
        empty_label='Any',
    )
    post_category = ModelMultipleChoiceFilter(
        label='Category',
        queryset=Category.objects.all(),
    )
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        empty_label='Any',
    )

    class Meta:
        model = Post

        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
            'rating': ['gt'],
        }
