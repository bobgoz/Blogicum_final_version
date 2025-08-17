from django.urls import path

from . import views

app_name = 'blog'


URLS = [
]
VIEWS = [
]
NAMES = [
]

urlpatterns = [
     path('', views.IndexListView.as_view(), name='index'),
     path('posts/<int:post_id>/',
          views.PostDetailView.as_view(), name='post_detail'),
     path('posts/<int:post_id>/edit/',
          views.EditPostUpdateView.as_view(), name='edit_post'),
     path('posts/<int:post_id>/delete/',
          views.DeletePostDeleteView.as_view(), name='delete_post'),
     path('posts/create/',
          views.CreatePostCreateView.as_view(), name='create_post'),
     path('category/<slug:category_slug>/',
          views.CategoryPostsListView.as_view(), name='category_posts'),
     path('profile/<slug:username>/',
          views.ProfileListView.as_view(), name='profile'),
     path('edit/', views.UserUpdateView.as_view(), name='edit_profile',),
     path('post/<int:post_id>/', 
          views.AddCommentCreateView.as_view(), name='add_comment'),
     path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
          views.EditCommentUpdateView.as_view(), name='edit_comment'),
     path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
          views.DeleteCommentDeleteView.as_view(), name='delete_comment'),
]
