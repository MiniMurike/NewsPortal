from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    PostList, PostDetail, PostSearch
)


urlpatterns = [
    path('', PostList.as_view(), name='post_lists'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearch.as_view(), name='post_search'),
]
