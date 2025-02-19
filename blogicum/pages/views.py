from django.shortcuts import render


def page_not_found_404(request, exception):
    """Переопределенная страницы ошибки 404"""
    return render(request, 'pages/404.html', status=404)


def server_error_500(request):
    """Переопределенная страницы ошибки 500"""
    return render(request, 'pages/500.html', status=500)


def csrf_failure_403(request, reason=''):
    """Переопределенная страницы ошибки 403"""
    return render(request, 'pages/403csrf.html', status=403)
