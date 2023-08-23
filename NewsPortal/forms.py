from django import forms
from .models import Post


class PostNewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
        ]

