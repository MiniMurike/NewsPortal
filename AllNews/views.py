from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView
)
from django.views.generic.edit import FormMixin

from .forms import CreateCommentForm
from .models import Post, CATEGORY_TYPES, Category, Comment, CommentReaction
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


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = CreateCommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        qs = Category.objects.filter(postcategory__post=self.object)

        result = []
        for item in qs:
            result.append(str(item))

        result = ', '.join(result)

        context['category'] = result
        context['post'].type = CATEGORY_TYPES[context['post'].type][1]

        context['comments'] = Comment.objects.filter(post=self.object.id).order_by('-rating', '-date')

        context['form'] = CreateCommentForm(initial={
            'post': self.object.id,
            'user': self.request.user
        })

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        comment_id = request.POST.get('comment_id')
        post_id = Comment.objects.get(id=comment_id).post_id

        # Если юзер - аноним
        if request.user.is_anonymous:
            return HttpResponseRedirect(f'/allnews/{post_id}')

        # Обработчик при создании коммента
        if action == 'create_comment':
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        comment_reaction = None
        comment = Comment.objects.get(id=comment_id)

        # Получаем реакцию юзера на коммент
        if CommentReaction.objects.filter(comment=comment_id).values('user') and \
                request.user.id is CommentReaction.objects.filter(comment=comment_id).values('user')[0]['user']:
            comment_reaction = CommentReaction.objects.get(
                comment=comment_id,
                user=request.user
            ).reaction

        # Если событие - лайк
        if action == 'like':
            if comment_reaction is None:
                CommentReaction.objects.create(
                    comment=comment,
                    user=request.user,
                    reaction='l',
                )
                comment.like()

            elif comment_reaction == 'd':
                CommentReaction.objects.filter(
                    comment=comment_id,
                    user=request.user,
                ).delete()
                CommentReaction.objects.create(
                    comment=comment,
                    user=request.user,
                    reaction='l',
                )
                comment.like() # Убираем последствия старого дизлайка
                comment.like() # Даём эффект лайка

            elif comment_reaction == 'l':
                CommentReaction.objects.filter(
                    comment=comment_id,
                    user=request.user,
                ).delete()
                comment.dislike()
                pass

        elif action == 'dislike':
            if comment_reaction is None:
                CommentReaction.objects.create(
                    comment=comment,
                    user=request.user,
                    reaction='d',
                )
                comment.dislike()

            elif comment_reaction == 'l':
                CommentReaction.objects.filter(
                    comment=comment_id,
                    user=request.user,
                ).delete()
                CommentReaction.objects.create(
                    comment=comment,
                    user=request.user,
                    reaction='d',
                )
                comment.dislike()  # Убираем последствия старого лайка
                comment.dislike()  # Даём эффект дизлайка

            elif comment_reaction == 'd':
                CommentReaction.objects.filter(
                    comment=comment_id,
                    user=request.user,
                ).delete()
                comment.like()

        return HttpResponseRedirect(f'/allnews/{post_id}')

    def get_success_url(self):
        return reverse('post_detail', kwargs={
            'pk': self.object.id
        })

    def form_valid(self, form):
        form.save()
        return super(PostDetail, self).form_valid(form)

    # def get_object(self, *args, **kwargs):
    #     obj = cache.get(f'post-{self.kwargs["pk"]}', None)
    #
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post-{self.kwargs["pk"]}', obj)
    #
    #     return obj


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


class PostArticleCreate(LoginRequiredMixin, CreateView):
    permission_required = ('AllNews.add_post',)

    form_class = CreateCommentForm
    model = Comment
    template_name = 'comment_create.html'
