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
    cek_pending = Current.objects.filter(status='pending').count()
    nama_layanan = Antrian.objects.filter(code_layanan=code).values()[
        0]['nama_layanan']
    context = {}
    context['page_title'] = 'Halaman Control'
    context['nama_layanan'] = nama_layanan
    if cek_pending == 0:
        context['pending_stat'] = 'none'
    elif cek_pending != 0:
        pending_queue = Current.objects.filter(
            status='pending').filter(jenis_layanan=code)
        context['pending_stat'] = 'check'
        context['pending_queue'] = pending_queue
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

            context['layanan'] = code
            context['now'] = curr
            context['total'] = tot
            context['active'] = active_queue
            context['stat'] = 'open'

        else:
            context['layanan'] = code
            context['now'] = curr
            context['total'] = tot
            context['active'] = "NoServing"
            context['stat'] = 'open'

        return render(request, 'control/detail.html', context)
    elif cek > 0 and non_active == 0:  # kondisi antrian semua done sisa 1 curr serve
        cek_active = Current.objects.filter(
            jenis_layanan=code).filter(status='active').count()
        if cek_active > 0:
            active = Current.objects.filter(jenis_layanan=code).filter(
                status='active').values()
            active_queue = active[0]['no_antrian']

            context['layanan'] = code
            context['now'] = "Habis"
            context['total'] = 0
            context['active'] = active_queue
            context['stat'] = 'closed'

        else:

            context['layanan'] = code
            context['now'] = "Habis"
            context['total'] = 0
            context['active'] = "NoServing"
            context['stat'] = 'closed'

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
        tot = request.POST['total']
        #print(onCall, stat, tot)
        url = '/control/detail/'+line
        if stat == 'open':  # jika sisa antrian masih ada
            if int(onCall) == 1:
                    # update on Call Queue
                active_ct = Current.objects.filter(
                    jenis_layanan=line).filter(status='active').count()
                if active_ct != 0:
                    active_left = Current.objects.filter(
                        jenis_layanan=line).filter(status='active').values()
                    active_left_id = active_left[0]['no_antrian']
                    Current.objects.filter(no_antrian=active_left_id).filter(
                        jenis_layanan=line).update(status='done')
                    Current.objects.filter(no_antrian=onCall).filter(
                        jenis_layanan=line).update(status='active')
                elif active_ct == 0:
                    Current.objects.filter(no_antrian=onCall).filter(
                        jenis_layanan=line).update(status='active')
            elif int(onCall) > 1:
                prev_call = int(onCall) - 1
                cek_prev = Current.objects.filter(no_antrian=prev_call).filter(
                    jenis_layanan=line).values()
                prev_status = cek_prev[0]['status']
                if prev_status == 'active':
                    Current.objects.filter(no_antrian=prev_call).filter(
                        jenis_layanan=line).update(status='done')
                    Current.objects.filter(no_antrian=onCall).filter(
                        jenis_layanan=line).update(status='active')
                elif prev_status == 'pending':
                    active_ct = Current.objects.filter(
                        jenis_layanan=line).filter(status='active').count()
                    if active_ct != 0:
                        active_left = Current.objects.filter(
                            jenis_layanan=line).filter(status='active').values()
                        active_left_id = active_left[0]['no_antrian']
                        Current.objects.filter(no_antrian=active_left_id).filter(
                            jenis_layanan=line).update(status='done')
                        Current.objects.filter(no_antrian=onCall).filter(
                            jenis_layanan=line).update(status='active')
                    elif active_ct == 0:
                        Current.objects.filter(no_antrian=onCall).filter(
                            jenis_layanan=line).update(status='active')
                elif prev_status == 'done':
                    active_ct = Current.objects.filter(
                        jenis_layanan=line).filter(status='active').count()
                    if active_ct != 0:
                        active_left = Current.objects.filter(
                            jenis_layanan=line).filter(status='active').values()
                        active_left_id = active_left[0]['no_antrian']
                        Current.objects.filter(no_antrian=active_left_id).filter(
                            jenis_layanan=line).update(status='done')
                        Current.objects.filter(no_antrian=onCall).filter(
                            jenis_layanan=line).update(status='active')
                    elif active_ct == 0:
                        Current.objects.filter(no_antrian=onCall).filter(
                            jenis_layanan=line).update(status='active')
        elif stat == 'closed':  # jika sisa antrian sudah 0
            if onCall == 'NoServing':
                return redirect('control:control')
            elif onCall != 'NoServing':
                active_ct = Current.objects.filter(
                    jenis_layanan=line).filter(status='active').count()
                if active_ct != 0:
                    active_left = Current.objects.filter(
                        jenis_layanan=line).filter(status='active').values()
                    active_left_id = active_left[0]['no_antrian']
                    Current.objects.filter(no_antrian=active_left_id).filter(
                        jenis_layanan=line).update(status='done')
                    Current.objects.filter(no_antrian=onCall).filter(
                        jenis_layanan=line).update(status='active')
                elif active_ct == 0:
                    Current.objects.filter(no_antrian=onCall).filter(
                        jenis_layanan=line).update(status='active')

        return redirect(str(url))
    else:
        print('GK MASUK')
        return redirect('control:control')


def skip(request, layanan, queue):
    line = layanan
    url = '/control/detail/'+line
    if queue != 'NoServing':
        Current.objects.filter(jenis_layanan=layanan).filter(
            no_antrian=queue).update(status='pending')
    else:
        return redirect(str(url))

    return redirect(str(url))


def finish(request, layanan, queue):
    line = layanan
    url = '/control/detail/'+line
    print(layanan, queue)
    if queue != 'NoServing':
        Current.objects.filter(jenis_layanan=layanan).filter(
            no_antrian=queue).update(status='done')

    return redirect(str(url))
