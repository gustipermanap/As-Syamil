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
from pengguna.daftar import DaftarFilterMixin
from pengguna.notifikasi import catat_akses
from pengguna.rapor_pdf import buat_pdf_rapor
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
        ctx['izin_diajukan'] = Izin.objects.filter(status='diajukan').count()
        ctx['tagihan_jatuh_tempo'] = Tagihan.objects.filter(
            jatuh_tempo__lt=hari,
        ).exclude(status__in=['lunas', 'batal']).count()
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
            ctx['izin'] = Izin.objects.filter(santri=santri).order_by('-mulai')[:10]
            ctx['nilai'] = Penilaian.objects.filter(santri=santri).select_related('mapel', 'periode').order_by('-id')[:20]
            ctx['tagihan'] = Tagihan.objects.filter(santri=santri).exclude(status='batal')
        return ctx


@login_required(login_url='/masuk/')
def rapor_html(request, santri_id):
    santri = get_object_or_404(Santri, pk=santri_id)
    wali = getattr(request.user, 'wali_santri', None)
    boleh = request.user.is_superuser or user_punya_grup(request.user, ['tata_usaha', 'mudir'])
    if wali and santri.wali_id == wali.id:
        boleh = True
    akun = santri_portal(request.user)
    if akun and akun.pk == santri.pk:
        boleh = True
    if not boleh:
        return HttpResponseForbidden('Tidak berhak melihat rapor santri ini.')
    nilai = Penilaian.objects.filter(santri=santri).select_related('mapel', 'periode')
    periode_id = request.GET.get('periode')
    if periode_id:
        nilai = nilai.filter(periode_id=periode_id)
    catat_akses(request.user, 'lihat_rapor', objek=santri.nomor_induk_santri, ringkas='rapor')
    pengaturan = Pengaturan.get()
    if request.GET.get('format') == 'pdf':
        return buat_pdf_rapor(santri, list(nilai), pengaturan)
    return render(request, 'pengguna/rapor.html', {
        'santri': santri,
        'nilai': nilai,
        'pengaturan': pengaturan,
    })


class DaftarPengguna(DaftarFilterMixin, OperasiMixin, ListView):
    model = User
    template_name = 'pengguna/pengguna_list.html'
    context_object_name = 'daftar'
    search_fields = ('username', 'email', 'first_name', 'last_name')
    boolean_filters = {'aktif': 'is_active'}
    cari_placeholder = 'Nama pengguna atau email'
    export_filename = 'pengguna.xlsx'
    export_columns = [
        ('Username', 'username'),
        ('Email', 'email'),
        ('Aktif', 'is_active'),
        ('Staf', 'is_staff'),
    ]
    filter_fields = [
        {'name': 'aktif', 'label': 'Aktif', 'choices': [('1', 'Aktif'), ('0', 'Nonaktif')]},
    ]
    aksi_massal_pilihan = [
        ('aktifkan', 'Aktifkan'),
        ('nonaktifkan', 'Nonaktifkan'),
    ]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('groups').order_by('username')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not (
            request.user.is_superuser or user_punya_grup(request.user, [GRUP_TU, 'mudir'])
        ):
            return HttpResponseForbidden('Hanya Tata Usaha yang mengelola pengguna.')
        return super().dispatch(request, *args, **kwargs)

    def bulk_aktifkan(self, ids):
        n = User.objects.filter(pk__in=ids).update(is_active=True)
        messages.success(self.request, f'{n} akun diaktifkan.')

    def bulk_nonaktifkan(self, ids):
        n = User.objects.filter(pk__in=ids).exclude(pk=self.request.user.pk).update(is_active=False)
        messages.success(self.request, f'{n} akun dinonaktifkan.')


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


@login_required(login_url='/masuk/')
def daftar_notifikasi(request):
    from .models import Notifikasi
    qs = Notifikasi.objects.filter(penerima=request.user)
    if request.method == 'POST':
        qs.filter(dibaca=False).update(dibaca=True)
        messages.success(request, 'Semua notifikasi ditandai sudah dibaca.')
        return redirect('pengguna:notifikasi')
    return render(request, 'pengguna/notifikasi.html', {'daftar': qs[:80]})


def privasi(request):
    return render(request, 'pengguna/privasi.html', {'pengaturan': Pengaturan.get()})
