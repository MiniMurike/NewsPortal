from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Сбор рейтинга постов автора
        query = Post.objects.filter(author__user=self.user).values('rating')
        result = 0

        for value in query:
            result += value['rating']
        result *= 3

        # Сбор рейтинга комментариев автора
        query = Comment.objects.filter(user=self.user).values('rating')

        for value in query:
            result += value['rating']

        # Сбор рейтинга комментариев постов автора
        query = Comment.objects.filter(post__author__user=self.user).values('rating')

        for value in query:
            result += value['rating']

        self.rating = result
        self.save()


CATEGORY_CATEGORIES = [
    ('spo', 'Спорт'),
    ('pol', 'Политика'),
    ('edu', 'Образование'),
    ('sci', 'Наука')
]


class Category(models.Model):
    category = models.CharField(max_length=3, choices=CATEGORY_CATEGORIES, unique=True, default='edu')


CATEGORY_TYPES = [
    (0, 'Статья'),
    (1, 'Новость')
]


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    # Можно сделать и через булево значение, но вдруг будет больше типов постов?
    type = models.IntegerField(default=0, choices=CATEGORY_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    post_category = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        return f'{self.text[:123]}...'

    def __str__(self):
        return f'{self.title}: {self.preview}'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
