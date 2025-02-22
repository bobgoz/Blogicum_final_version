from django.urls import path

from . import views

app_name = 'blog'


URLS = [
    '',
    'posts/<int:post_id>/',
    'posts/<int:post_id>/edit/',
    'posts/<int:post_id>/delete/',
    'posts/create/',
    'category/<slug:category_slug>/',
    'profile/<slug:username>/',
    'edit/',
    'post/<int:post_id>/',
    'posts/<int:post_id>/edit_comment/<int:comment_id>/',
    'posts/<int:post_id>/delete_comment/<int:comment_id>/',
]
VIEWS = [
    views.IndexListView.as_view(),
    views.PostDetailView.as_view(),
    views.EditPostUpdateView.as_view(),
    views.DeletePostDeleteView.as_view(),
    views.CreatePostCreateView.as_view(),
    views.CategoryPostsListView.as_view(),
    views.ProfileListView.as_view(),
    views.UserUpdateView.as_view(),
    views.AddCommentCreateView.as_view(),
    views.EditCommentUpdateView.as_view(),
    views.DeleteCommentDeleteView.as_view(),
]
NAMES = [
    'index',
    'post_detail',
    'edit_post',
    'delete_post',
    'create_post',
    'category_posts',
    'profile',
    'edit_profile',
    'add_comment',
    'edit_comment',
    'delete_comment',
]

urlpatterns = [
    path(URLS[0], VIEWS[0], name=NAMES[0],
         ),
    path(URLS[1], VIEWS[1], name=NAMES[1],
         ),
    path(URLS[2], VIEWS[2], name=NAMES[2],
         ),
    path(URLS[3], VIEWS[3], name=NAMES[3],
         ),
    path(URLS[4], VIEWS[4], name=NAMES[4],
         ),
    path(URLS[5], VIEWS[5], name=NAMES[5],
         ),
    path(URLS[6], VIEWS[6], name=NAMES[6],
         ),
    path(URLS[7], VIEWS[7], name=NAMES[7],
         ),
    path(URLS[8], VIEWS[8], name=NAMES[8],
         ),
    path(URLS[9], VIEWS[9], name=NAMES[9],
         ),
    path(URLS[10], VIEWS[10], name=NAMES[10],
         ),
]
