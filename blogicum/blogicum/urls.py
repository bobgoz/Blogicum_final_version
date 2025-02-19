from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from blog.views import UserPasswordChangeView, RegistrationUser


handler404 = 'pages.views.page_not_found_404'
handler500 = 'pages.views.server_error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path(
        'auth/password_change/',
        UserPasswordChangeView.as_view(),
        name='password_change',
    ),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        RegistrationUser.as_view(),
        name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
