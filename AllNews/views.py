from django.db.models import Count
from django.views.generic import (
    ListView, DetailView
)

from .models import Post, CATEGORY_TYPES, Category, PostCategory
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = 'date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.annotate(count=Count('title'))

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Category.objects.filter(postcategory__post=self.object)

        result = []
        for item in qs:
            result.append(str(item))

        result = ', '.join(result)

        context['category'] = result
        context['post'].type = CATEGORY_TYPES[context['post'].type][1]
        
        return context


class PostSearch(ListView):
    model = Post
    ordering = 'date'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context
