from django.shortcuts import render, redirect
import layanan
from layanan.models import Current, Antrian
from layanan.forms import CurrentForm
# Create your views here.


def display(request):
    queue = Current.objects.filter(status='active')
    context = {
        'page_title': 'Display',
        'queue': queue,
    }
    return render(request, 'customer/index.html', context)
