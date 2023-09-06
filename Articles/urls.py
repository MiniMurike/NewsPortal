from django.urls import path
from .views import (
    PostArticleUpdate, PostArticleCreate, PostArticleDelete
)


urlpatterns = [
    path('create/', PostArticleCreate.as_view(), name='post_article_create'),
    path('<int:pk>/update/', PostArticleUpdate.as_view(), name='post_article_update'),
    path('<int:pk>/delete/', PostArticleDelete.as_view(), name='post_article_delete'),
]