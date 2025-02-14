from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django import forms
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm




from .models import Post, Category
from .forms import PostForm, UserChangeForm, CommentForm
from .models import User


class IndexListView(ListView):
    queryset = Post.posts_objects.all()
    ordering = '-pub_date'
    paginate_by = 5
    template_name = 'blog\index.html'



def add_comment(request, id_comment):
    post = get_object_or_404(Post.objects.all(), pk=id_comment)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.save()
    return redirect('blog:post_detail', pk=id_comment)

# def index(request):
#     post_list = Post.posts_objects.order_by('-pub_date')[0:5]
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.posts_objects.all(), id=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)

class DeletePostDeleteView(DeleteView):
    model = Post


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.category_objects.all(),
        slug=category_slug
    )
    post_list = Post.posts_objects.filter(
        category=category,
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)

# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = ''

class ProfileDetailView(DetailView):
    # pass
    model = User
    # queryset = Post.objects.select_related('User').all()
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'
    template_name = 'blog/profile.html'

# def profile(request, username):
#     object = get_object_or_404()
    
def profile(request, username):
    profile = get_object_or_404(User.objects.all(), username=username)

    posts = Post.objects.filter(author=profile).order_by('id')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
        }
    return render(request, 'blog\profile.html', context)

    
# class EditProfile(UpdateView):
#     model = User
#     form_class = UserChangeForm

#     def get_object(self, queryset = None):
#         return self.request.user
    
# def edit_post(request, post_id=None):
#     if post_id is not None:
#         post = get_object_or_404(Post.objects.all(), pk=post_id)
#         return render(request, )
#     else:
class EditPostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    # template_name = 
    # success_url = reverse_lazy('blog:')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:edit_profile')

    def get_object(self, queryset = None):
        return self.request.user

    
# def edit_user(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save() 
#             return redirect('blog:index')  
#     else:
#         form = UserChangeForm(instance=user)
#     context = {'form': form}

#     return render(request, 'blog/user.html', context)

class CreatePostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog\create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

