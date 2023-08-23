from django_filters import (
    FilterSet, DateTimeFilter, ModelMultipleChoiceFilter, ModelChoiceFilter, ChoiceFilter, CharFilter)

from .models import Post, PostCategory, Author, CATEGORY_TYPES
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
    category = ModelMultipleChoiceFilter(
        label='Category',
        field_name='postcategory',
        queryset=PostCategory.objects.all(),
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
