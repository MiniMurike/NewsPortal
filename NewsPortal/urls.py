from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch, PostNewsCreate, PostNewsUpdate, PostNewsDelete, PostArticleCreate,
    PostArticleDelete
)


urlpatterns = [
    path('', PostList.as_view(), name='post_lists'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearch.as_view(), name='post_search'),

    path('news/create/', PostNewsCreate.as_view(), name='post_news_create'),
    path('news/<int:pk>/update/', PostNewsUpdate.as_view(), name='post_news_update'),
    path('news/<int:pk>/delete/', PostNewsDelete.as_view(), name='post_news_delete'),

    path('article/create/', PostArticleCreate.as_view(), name='post_article_create'),
    path('article/<int:pk>/update/', PostNewsUpdate.as_view(), name='post_article_update'),
    path('article/<int:pk>/delete/', PostArticleDelete.as_view(), name='post_article_delete'),
]
