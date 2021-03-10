from django.shortcuts import render, redirect
import layanan
from layanan.models import Current, Antrian
from layanan.forms import CurrentForm
# Create your views here.


def display(request):
    context = {}
    context['page_title'] = 'Display'
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
