from django.shortcuts import render, redirect
from .models import Antrian
from .models import Current
# Create your views here.
from .forms import CurrentForm
import copy


def list(request):
    layanan = Antrian.objects.all()
    context = {
        'page_title': 'Sosial Media',
        'layanan': layanan,
    }
    return render(request, 'index.html', context)


def queue(request, q_id):
    cek = Current.objects.filter(jenis_layanan=q_id).count()

    if cek > 0:
        curr = Current.objects.filter(
            jenis_layanan=q_id).order_by('-no_antrian')[0]
        a = str(curr)
        curr_val = int(a)
        next_queue = curr_val + 1
        jenis_layanan = q_id
        status = 'non-active'
        queue = Current(no_antrian=next_queue,
                        jenis_layanan=jenis_layanan, status=status)
        queue.save()
    else:
        no_antrian = 1
        jenis_layanan = q_id
        status = 'non-active'

        queue = Current(no_antrian=no_antrian,
                        jenis_layanan=jenis_layanan, status=status)
        queue.save()
    return redirect('layanan:list')
