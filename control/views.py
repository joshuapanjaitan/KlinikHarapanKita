from django.shortcuts import render, redirect
import layanan
from layanan.models import Current, Antrian
from layanan.forms import CurrentForm
# Create your views here.


def control(request):
    layanan = Antrian.objects.all()
    context = {
        'page_title': 'Halaman Control',
        'layanan': layanan
    }
    return render(request, 'control/index.html', context)


def detail(request, code):
    # cek apakah sudah ada yg ngantri ?
    cek = Current.objects.filter(jenis_layanan=code).count()
    non_active = Current.objects.filter(
        jenis_layanan=code).filter(status='non-active').count()
    if cek > 0 and non_active > 0:
        curr = Current.objects.filter(jenis_layanan=code).filter(
            status='non-active').order_by('no_antrian')[0]
        tot = Current.objects.filter(jenis_layanan=code).filter(
            status='non-active').count()
        cek_active = Current.objects.filter(
            jenis_layanan=code).filter(status='active').count()
        if cek_active > 0:
            active = Current.objects.filter(jenis_layanan=code).filter(
                status='active').values()
            active_queue = active[0]['no_antrian']
            context = {
                'layanan': code,
                'now': curr,
                'total': tot,
                'active': active_queue,
                'stat': 'open',
            }
        else:
            context = {
                'layanan': code,
                'now': curr,
                'total': tot,
                'active': "No Serving",
                'stat': 'open',
            }
        return render(request, 'control/detail.html', context)
    elif cek > 0 and non_active == 0:  # kondisi antrian semua done sisa 1 curr serve
        cek_active = Current.objects.filter(
            jenis_layanan=code).filter(status='active').count()
        if cek_active > 0:
            active = Current.objects.filter(jenis_layanan=code).filter(
                status='active').values()
            active_queue = active[0]['no_antrian']
            context = {
                'layanan': code,
                'now': "Habis",
                'total': 0,
                'active': active_queue,
                'stat': 'closed',
            }
        else:
            context = {
                'layanan': code,
                'now': "Habis",
                'total': 0,
                'active': "No Serving",
                'stat': 'closed',
            }
        return render(request, 'control/detail.html', context)

    else:
        print("Antrian pada layanan ini belum ada")
        return redirect('control:control')
    return redirect('control:control')


def call(request):
    if request.method == 'POST':
        onCall = request.POST['onCall']
        line = request.POST['code_layanan']
        stat = request.POST['stat']
        url = '/control/detail/'+line
        if stat == 'open':
            if int(onCall) == 1:
                # update on Call Queue
                Current.objects.filter(no_antrian=onCall).filter(
                    jenis_layanan=line).update(status='active')
            elif int(onCall) > 1:
                prev_call = int(onCall) - 1
                Current.objects.filter(no_antrian=prev_call).filter(
                    jenis_layanan=line).update(status='done')
                Current.objects.filter(no_antrian=onCall).filter(
                    jenis_layanan=line).update(status='active')
        elif stat == 'closed':

            if onCall == 'No Serving':
                return redirect('control:control')
            else:
                Current.objects.filter(no_antrian=onCall).filter(
                    jenis_layanan=line).update(status='done')
        return redirect(str(url))
    else:
        print('GK MASUK')
        return redirect('control:control')
