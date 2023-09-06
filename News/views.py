from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView
)

from django.contrib.auth.mixins import PermissionRequiredMixin

from AllNews.models import Post
from AllNews.forms import PostNewsForm


class PostNewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('AllNews.add_post',)

    form_class = PostNewsForm
    model = Post
    template_name = 'post_news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 1

        return super().form_valid(form)


class PostNewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('AllNews.change_post',)

    form_class = PostNewsForm
    model = Post
    template_name = 'post_news_create.html'


class PostNewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('AllNews.delete_post',)

    model = Post
    template_name = 'post_news_delete.html'
    success_url = reverse_lazy('post_lists')
