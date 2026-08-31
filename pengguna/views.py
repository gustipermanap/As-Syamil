from django.contrib.auth.decorators import login_required
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView

from akademik.models import Absensi, JadwalSlot, Penilaian
from kesiswaan.models import AbsensiAsrama, Izin, PenempatanKamar, Santri
from kesiswaan.services import anak_wali, santri_portal
from keuangan.models import Tagihan
from lembaga.models import Pengaturan
from ppdb.models import GelombangPPDB
from tahfidz.models import ProgressHafalan, SetoranHafalan
from WebApp.models import Pendaftaran
from .forms_util import kelas_bootstrap
from .mixins import OperasiMixin, SantriPortalMixin, WaliMixin, butuh_operasi
from .models import GRUP_SANTRI, GRUP_TU, GRUP_WALI
from .services import pastikan_grup, user_punya_grup


def masuk(request):
    pastikan_grup()
    error = ''
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
        )
        if user is not None:
            login(request, user)
            if user_punya_grup(user, GRUP_WALI) and not user_punya_grup(user, ['mudir', 'tata_usaha']):
                return redirect('pengguna:wali')
            if user_punya_grup(user, GRUP_SANTRI) and Pengaturan.get().portal_santri_aktif:
                return redirect('pengguna:santri')
            return redirect('pengguna:operasi')
        error = 'Nama pengguna atau sandi salah, atau akun nonaktif.'
    return render(request, 'pengguna/masuk.html', {'error': error})


def keluar(request):
    logout(request)
    return redirect('pengguna:masuk')


class OperasiDasbor(OperasiMixin, TemplateView):
    template_name = 'pengguna/operasi.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hari = date.today()
        ctx['pengaturan'] = Pengaturan.get()
        ctx['santri_aktif'] = Santri.objects.filter(status='aktif').count()
        ctx['ppdb_masuk'] = Pendaftaran.objects.filter(status='dikirim').count()
        ctx['gelombang'] = GelombangPPDB.objects.order_by('-mulai')[:5]
        ctx['setoran_hari_ini'] = SetoranHafalan.objects.filter(tanggal=hari).count()
        ctx['tunggakan'] = Tagihan.objects.exclude(status='lunas').exclude(status='batal').count()
        ctx['alpa'] = Absensi.objects.filter(status='alpa').count()
        ctx['hadir_hari_ini'] = Absensi.objects.filter(pertemuan__tanggal=hari, status='hadir').count()
        ctx['hadir_asrama_hari_ini'] = AbsensiAsrama.objects.filter(tanggal=hari, status='hadir').count()
        pegawai = getattr(self.request.user, 'pegawai', None)
        if pegawai:
            ctx['jadwal_hari_ini'] = JadwalSlot.objects.filter(
                pengampu=pegawai, hari=hari.weekday(),
            ).select_related('rb', 'mapel')
        else:
            ctx['jadwal_hari_ini'] = JadwalSlot.objects.none()
        return ctx


class WaliDasbor(WaliMixin, TemplateView):
    template_name = 'pengguna/wali.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        anak = anak_wali(self.request.user)
        ringkas = []
        for s in anak:
            ringkas.append({
                'santri': s,
                'kamar': PenempatanKamar.objects.filter(santri=s, keluar__isnull=True).select_related('kamar__gedung').first(),
                'rb': list(s.keanggotaan_rb.select_related('rb')),
                'absensi': Absensi.objects.filter(santri=s).select_related('pertemuan').order_by('-pertemuan__tanggal')[:5],
            })
        ctx['anak'] = anak
        ctx['ringkas'] = ringkas
        ctx['tagihan'] = Tagihan.objects.filter(santri__in=anak).exclude(status='batal')
        ctx['nilai'] = Penilaian.objects.filter(santri__in=anak).order_by('-id')[:20]
        ctx['izin'] = Izin.objects.filter(santri__in=anak).order_by('-mulai')[:10]
        ctx['setoran'] = SetoranHafalan.objects.filter(santri__in=anak).order_by('-tanggal')[:10]
        return ctx


class SantriDasbor(SantriPortalMixin, TemplateView):
    template_name = 'pengguna/santri.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        santri = santri_portal(self.request.user)
        ctx['santri'] = santri
        if santri:
            ctx['setoran'] = SetoranHafalan.objects.filter(santri=santri)[:10]
            ctx['progress'] = ProgressHafalan.objects.filter(santri=santri).first()
            ctx['izin'] = __import__('kesiswaan.models', fromlist=['Izin']).Izin.objects.filter(
                santri=santri,
            ).order_by('-mulai')[:10]
        return ctx


@login_required(login_url='/masuk/')
def rapor_html(request, santri_id):
    santri = get_object_or_404(Santri, pk=santri_id)
    wali = getattr(request.user, 'wali_santri', None)
    boleh = request.user.is_superuser or user_punya_grup(request.user, ['tata_usaha', 'mudir'])
    if wali and santri.wali_id == wali.id:
        boleh = True
    if not boleh:
        return HttpResponseForbidden('Tidak berhak melihat rapor santri ini.')
    nilai = Penilaian.objects.filter(santri=santri)
    periode_id = request.GET.get('periode')
    if periode_id:
        nilai = nilai.filter(periode_id=periode_id)
    return render(request, 'pengguna/rapor.html', {
        'santri': santri,
        'nilai': nilai,
        'pengaturan': Pengaturan.get(),
    })


class DaftarPengguna(OperasiMixin, ListView):
    template_name = 'pengguna/pengguna_list.html'
    context_object_name = 'daftar'

    def get_queryset(self):
        return User.objects.all().order_by('username')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not (
            request.user.is_superuser or user_punya_grup(request.user, [GRUP_TU, 'mudir'])
        ):
            return HttpResponseForbidden('Hanya Tata Usaha yang mengelola pengguna.')
        return super().dispatch(request, *args, **kwargs)


@butuh_operasi
def reset_sandi(request, pk):
    if not (request.user.is_superuser or user_punya_grup(request.user, [GRUP_TU, 'mudir'])):
        return HttpResponseForbidden('Hanya Tata Usaha yang boleh mereset sandi.')
    target = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        sandi = request.POST.get('sandi', '')
        if len(sandi) < 6:
            messages.error(request, 'Sandi minimal 6 karakter.')
        else:
            target.set_password(sandi)
            target.save()
            messages.success(request, f'Sandi {target.username} sudah diubah.')
            return redirect('pengguna:daftar')
    return render(request, 'pengguna/form_umum.html', {
        'judul': f'Reset sandi {target.username}',
        'form_html': '<div class="mb-3"><label class="form-label">Sandi baru</label>'
                     '<input class="form-control" type="password" name="sandi" required minlength="6"></div>',
        'submit_label': 'Simpan sandi',
    })
