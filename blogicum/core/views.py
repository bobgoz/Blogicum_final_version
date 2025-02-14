from django.shortcuts import render


def csrf_failure_403(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

def page_not_found_404(request, exception):
    return render(request, 'pages/404.html', status=404)

def server_error_500(request):
    return render(request, 'page/500.html', status=500)