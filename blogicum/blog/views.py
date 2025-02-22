from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Category, Comment, User
from .forms import UserChangeForm, CommentForm
from blog.mixins import (
    OnlyAuthorMixinForUser,
    OnlyAuthorMixinForModels,
    DeleteAndUpdateCommentsMixin,
    GetSuccessUrlMixin,
)

PAGE_PAGINATION = 10


class RegistrationUser(CreateView):
    """CBV для создания формы регистрации пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class UserPasswordChangeView(
    LoginRequiredMixin,
    OnlyAuthorMixinForUser,
    PasswordChangeView,
):
    """Переопределение дефолтной формы восстановления
    пароля для получения объекта пользователя.
    """

    def get_object(self):
        return self.request.user


class IndexListView(ListView):
    """CBV для отображения списка постов главной страницы"""

    queryset = Post.objects_manager.posts_object_with_annotate()
    paginate_by = PAGE_PAGINATION
    template_name = 'blog/index.html'


class AddCommentCreateView(LoginRequiredMixin, GetSuccessUrlMixin, CreateView):
    """CBV для добавления комментариев."""

    post_obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)


class PostDetailView(DetailView):
    """CBV для отображения поста в деталях"""

    model = Post
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(
            Post.objects.select_related('author'), pk=post_id)
        # Проверка, чтобы автору поста была доступна его публикация,
        # если категория не опубликована.
        if self.request.user.username == post.author.username:
            return post
        return get_object_or_404(Post.objects_manager.posts_objects(
        ).select_related('author'), pk=post_id)

    def get_context_data(self, **kwargs):
        # Передаём дополнительные переменные в контекст.
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            Comment.objects.select_related('author')
        )
        print(context)
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


class EditPostUpdateView(
    OnlyAuthorMixinForModels,
    LoginRequiredMixin,
    GetSuccessUrlMixin,
    UpdateView,
):
    """Класс для редактирования постов."""

    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверка для доступа к редактированию
        # постов только авторам постов.
        if self.object.author != self.request.user:
            return redirect('blog:post_detail', post_id=self.object.pk)
        return super().dispatch(request, *args, **kwargs)


class CategoryPostsListView(ListView):
    """CBV для отображения категорий постов"""

    category = None
    queryset = None
    paginate_by = PAGE_PAGINATION
    template_name = 'blog/category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category,
                                          slug=kwargs['category_slug'],
                                          is_published=True,
                                          )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        post_list = Post.objects_manager.posts_objects(
        ).filter(category=self.category).order_by('-pub_date')
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileListView(ListView):
    """CBV для отображения страницы профиля пользователя."""

    profile = None
    queryset = None
    template_name = 'blog/profile.html'
    paginate_by = PAGE_PAGINATION
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(User, username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    def get_queryset(self):
        if self.request.user == self.profile:
            return Post.objects_manager.posts_with_annotate(
            ).filter(author=self.profile)
        else:
            return Post.objects_manager.posts_object_with_annotate(
            ).filter(author=self.profile)


class UserUpdateView(OnlyAuthorMixinForUser, LoginRequiredMixin, UpdateView):
    """CBV для редактирования пользователя."""

    model = User
    form_class = UserChangeForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:edit_profile')

    def get_object(self):
        # Получение объекта текущего пользователя.
        return self.request.user


class CreatePostCreateView(LoginRequiredMixin, GetSuccessUrlMixin, CreateView):
    """CBV Для создания постов."""

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


class EditCommentUpdateView(
    LoginRequiredMixin,
    DeleteAndUpdateCommentsMixin,
    GetSuccessUrlMixin,
    UpdateView,
):
    """CBV для редактирования комментариев."""

    comment = None
    post_obj = None
    form_class = CommentForm


class DeleteCommentDeleteView(
    LoginRequiredMixin,
    DeleteAndUpdateCommentsMixin,
    GetSuccessUrlMixin,
    DeleteView,
):
    """CBV для удаления коменнтариев."""

    model = Comment
