from django import forms

from .models import Post, CATEGORY_CATEGORIES, Category, Author, Comment


class PostNewsForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        label='Автор',
        queryset=Author.objects.all(),
        empty_label=None,
    )

    def __init__(self, *args, **kwargs):
        super(PostNewsForm, self).__init__(*args, **kwargs)
        self.fields['post_category'].label = 'Категории'
        self.fields['post_category'].queryset = Category.objects.all()

        # Формат (1, 'Название категории')
        self.fields['post_category'].choices = \
            [
                (index + 1, item[1]) for index, item in enumerate(CATEGORY_CATEGORIES)
            ]

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'post_category',
        ]

        labels = {
            'title': 'Заголовок',
            'text': 'Содержание',
        }


class CreateCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment

        fields = {
            'post',
            'user',
            'text',
        }

        widgets = {
            'post': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }
