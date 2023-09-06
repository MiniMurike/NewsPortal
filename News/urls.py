from django.urls import path
from .views import (
    PostNewsCreate, PostNewsUpdate, PostNewsDelete
)


urlpatterns = [
    path('create/', PostNewsCreate.as_view(), name='post_news_create'),
    path('<int:pk>/update/', PostNewsUpdate.as_view(), name='post_news_update'),
    path('<int:pk>/delete/', PostNewsDelete.as_view(), name='post_news_delete'),
]