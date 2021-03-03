from django.shortcuts import render


def index(request):
    context = {
        'title': 'Welcome Home',
        'heading': 'Selamat datang di Website Kami',
    }
    return render(request, 'index.html', context)
