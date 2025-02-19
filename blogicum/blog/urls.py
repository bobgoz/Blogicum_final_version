from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.EditPostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/', views.DeletePostDeleteView.as_view(), name='delete_post'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('edit/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('create_post/', views.CreatePostCreateView.as_view(), name='create_post'),
    path('comments/<int:pk>/',views.add_comment, name='add_comment'),
    path('post/<int:post_id>/comments/<int:comment_id>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('post/<int:post_id>/comments/<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    
]
