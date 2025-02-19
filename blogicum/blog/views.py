from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.utils.timezone import now

from .models import Post, Category, Comment
from .forms import PostForm, UserChangeForm, CommentForm
from .models import User

PAGE_PAGINATION = 10


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


class UserPasswordChangeView(
    LoginRequiredMixin,
    OnlyAuthorMixinForUser,
    PasswordChangeView,
):
    """Переопределение дефолтной формы восстановления
    паролядля получения объекта пользователя.
    """

    def get_object(self):
        return self.request.user


class IndexListView(ListView):
    """CBV для отображения списка постов главной страницы"""

    queryset = Post.posts_objects.annotate(comment_count=Count('comment'))
    ordering = '-pub_date'
    paginate_by = PAGE_PAGINATION
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_count'] = self.queryset
        return context


@login_required
def add_comment(request, post_id):
    """Функция для обработки POST запроса
    для добавления комментариев.
    """
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = post
        new_comment.save()
    return redirect('blog:post_detail', post_id)


def post_detail(request, post_id):
    post = get_object_or_404(Post.posts_objects.all(), id=post_id)
    context = {
        'post': post,
        'form': CommentForm(),
    }
    return render(request, 'blog/detail.html', context)


class PostDetailView(DetailView):
    """CBV для отображения поста в деталях"""

    model = Post
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        # Проверка, чтобы автору поста была доступна его публикация,
        # если категория не опубликована.
        # P.S. были перебраны многие варианты,
        # и именно этот работает (проходит тесты).
        if not (
            post.author == self.request.user
            or (post.is_published
                and post.category.is_published
                and post.pub_date <= now())
        ):
            raise Http404('Страница не найдена')
        else:
            return post

    def get_context_data(self, **kwargs):
        # Передаём дополнительные переменные в контекст.
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comment.select_related('author',
                                               'post',
                                               )
        )
        return context


class DeletePostDeleteView(
    OnlyAuthorMixinForModels,
    LoginRequiredMixin,
    DeleteView,
):
    """CBV для удаления постов."""

    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/create.html'


class EditPostUpdateView(
    OnlyAuthorMixinForModels,
    LoginRequiredMixin,
    UpdateView,
):
    """Класс для редактирования постов."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверка для доступа к редактированию
        # постов только авторам постов.
        if self.object.author != self.request.user:
            return redirect('blog:post_detail', post_id=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Перенаправляем пользователя
        # после POST запроса.
        return reverse_lazy(
            'blog:post_detail',
            kwargs={self.pk_url_kwarg: self.object.pk},
        )


def category_posts(request, category_slug):
    """Функция для отображения категорий постов."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = Post.posts_objects.order_by('-pub_date').filter(
        category=category,
    )

    paginator = Paginator(post_list, PAGE_PAGINATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def profile(request, username):
    """Функция для отображения пользователя"""
    profile = get_object_or_404(User, username=username)
    if request.user == profile:
        posts = Post.objects.filter(
            author=profile,
        ).order_by('-pub_date').annotate(comment_count=Count('comment'))
    else:
        posts = Post.posts_objects.filter(
            author=profile,
        ).order_by('-pub_date').annotate(comment_count=Count('comment'))

    paginator = Paginator(posts, PAGE_PAGINATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
        'comment_count': posts
    }
    return render(request, 'blog/profile.html', context)


class UserUpdateView(OnlyAuthorMixinForUser, LoginRequiredMixin, UpdateView):
    """CBV для редактирования пользователя."""

    model = User
    form_class = UserChangeForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:edit_profile')

    def get_object(self):
        # Получение объекта текущего пользователя.
        return self.request.user


class CreatePostCreateView(LoginRequiredMixin, CreateView):
    """CBV Для создания постов."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        # Передаем объект пользователя в форму.
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправляем пользователя после POST запроса.
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


@login_required
def edit_comment(request, post_id, comment_id):
    """Функция для редактирования комментариев."""
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    # Проверка для доступа к редактированию
    # комментариев только авторам комментариев.
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)
    form = CommentForm(request.POST or None, instance=comment)
    context = {
        'form': form,
        'post_id': post,
        'comment': comment,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
    else:
        return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Функция для удаления комментариев."""
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    # Проверка для доступа к удалению комментариев
    # только авторам комментариев.
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)
    context = {
        'post': post,
    }
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)
    else:
        return render(request, 'blog/comment.html', context)


class RegistrationUser(CreateView):
    """CBV для создания формы регистрации пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
