from django.shortcuts import render, redirect
import layanan
from layanan.models import Current, Antrian
from layanan.forms import CurrentForm
from datetime import datetime
# Create your views here.


def display(request):
    context = {}
    now = datetime.now().strftime('%H:%M:%S')
    context['page_title'] = 'Monitor - Lantai 1'
    context['myDate'] = now

    # bpjs
    bpjs = Current.objects.filter(status='active').filter(jenis_layanan='A')
    ct_bpjs = Current.objects.filter(
        status='active').filter(jenis_layanan='A').count()
    if ct_bpjs == 0:
        context['bpjs'] = '#'
    else:
        context['bpjs'] = bpjs

    # gigi
    gigi = Current.objects.filter(status='active').filter(jenis_layanan='B')
    ct_gigi = Current.objects.filter(
        status='active').filter(jenis_layanan='B').count()

    if ct_gigi == 0:
        context['gigi'] = '#'
    else:
        context['gigi'] = gigi

    # jantung
    jantung = Current.objects.filter(status='active').filter(jenis_layanan='C')
    ct_jantung = Current.objects.filter(
        status='active').filter(jenis_layanan='C').count()

    if ct_jantung == 0:
        context['jantung'] = '#'
    else:
        context['jantung'] = jantung

    """
    context = {
        'page_title': 'Display',
        'bpjs': bpjs,
        'gigi': gigi,
        'jantung': jantung,
    }
    """
    return render(request, 'customer/index.html', context)
