from django.urls import path
from django.views.generic import TemplateView


handler403 = 'pages.views.csrf_failure_403'

app_name = 'pages'

urlpatterns = [
    path(
        'about/',
        TemplateView.as_view(template_name='pages/about.html'),
        name='about'
    ),
    path(
        'rules/',
        TemplateView.as_view(template_name='pages/rules.html'),
        name='rules'
    ),
]
