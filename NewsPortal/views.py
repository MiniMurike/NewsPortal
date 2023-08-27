from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post
from .forms import PostNewsForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = 'date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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


# ------------------------------
# Взаимодействие с НОВОСТЯМИ
# ------------------------------


class PostNewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)

    form_class = PostNewsForm
    model = Post
    template_name = 'post_news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 1

        return super().form_valid(form)


class PostNewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)

    form_class = PostNewsForm
    model = Post
    template_name = 'post_news_create.html'


class PostNewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)

    model = Post
    template_name = 'post_news_delete.html'
    success_url = reverse_lazy('post_lists')


# ------------------------------
# Взаимодействие со СТАТЬЯМИ
# ------------------------------


class PostArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)

    form_class = PostNewsForm
    model = Post
    template_name = 'post_news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 0

        return super().form_valid(form)


class PostArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)

    model = Post
    template_name = 'post_article_delete.html'
    success_url = reverse_lazy('post_lists')
