from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from .models import Comment, Post
from .forms import PostForm


class OnlyAuthorMixinForUser(UserPassesTestMixin):
    """Тестер для проверки принадлежности объекта пользователя пользователю"""

    def test_func(self):
        object = self.get_object()
        return object == self.request.user


class OnlyAuthorMixinForModels(UserPassesTestMixin):
    """Тестер для проверки принадлежности объекта модели пользователю"""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class DeleteAndUpdateCommentsMixin():
    """Миксин для дополнения классов-обработчиков
    удаления и редактирования комментариев.
    """

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    # Расширяем dispatch, вводим проверку на принадлежность
    # объекта комментария пользователю, чтобы на первых
    # этапах обработки отсеять ненужных пользователей.
    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if self.request.user != comment.author:
            return redirect('blog:post_detail', kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class GetSuccessUrlMixin():
    """Миксин с функцией get_success_url для
    перенаправления пользователя после POST запроса
    """

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})
