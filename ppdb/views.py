from django import forms
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from akademik.models import RombonganBelajar
from kesiswaan.models import Kamar
from pengguna.daftar import DaftarFilterMixin
from pengguna.forms_util import kelas_bootstrap
from pengguna.mixins import OperasiMixin, butuh_operasi
from pengguna.models import GRUP_TU
from pengguna.services import user_punya_grup
from WebApp.models import Pendaftaran
from .models import GelombangPPDB
from .services import terima_menjadi_santri


class GelombangForm(forms.ModelForm):
    class Meta:
        model = GelombangPPDB
        fields = ['nama', 'mulai', 'selesai', 'kuota', 'status', 'biaya_pendaftaran', 'unit_tujuan']
        widgets = {
            'mulai': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'selesai': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class AntrianPPDB(DaftarFilterMixin, OperasiMixin, ListView):
    model = Pendaftaran
    template_name = 'ppdb/antrian.html'
    context_object_name = 'daftar'
    search_fields = ('nama_lengkap', 'kode_pendaftaran', 'nisn', 'nama_ayah', 'nama_ibu')
    exact_filters = {
        'status': 'status',
        'gelombang': 'gelombang_id',
        'jenis_kelamin': 'jenis_kelamin',
    }
    date_field = 'created_at'
    cari_placeholder = 'Nama, kode, NISN, orang tua'
    export_filename = 'ppdb.xlsx'
    export_columns = [
        ('Kode', 'kode_pendaftaran'),
        ('Nama', 'nama_lengkap'),
        ('JK', 'get_jenis_kelamin_display'),
        ('Gelombang', 'gelombang.nama'),
        ('Status', 'get_status_display'),
        ('Kota', 'kota_kabupaten'),
        ('HP', 'no_handphone'),
    ]
    aksi_massal_pilihan = [
        ('verifikasi', 'Ubah: Verifikasi'),
        ('berkas_kurang', 'Ubah: Berkas kurang'),
        ('tes', 'Ubah: Tes'),
        ('cadangan', 'Ubah: Cadangan'),
        ('ditolak', 'Ubah: Ditolak'),
    ]

    def get_filter_fields(self):
        return [
            {'name': 'status', 'label': 'Status', 'choices': Pendaftaran._meta.get_field('status').choices},
            {
                'name': 'gelombang',
                'label': 'Gelombang',
                'choices': [(g.pk, g.nama) for g in GelombangPPDB.objects.all()],
                'advanced': True,
            },
            {
                'name': 'jenis_kelamin',
                'label': 'Jenis kelamin',
                'choices': Pendaftaran.jenis_kelamin_choices,
                'advanced': True,
            },
        ]

    def get_queryset(self):
        return super().get_queryset().select_related('gelombang').order_by('-id')

    def _bulk_status(self, ids, status):
        n = Pendaftaran.objects.filter(pk__in=ids).exclude(status='diterima').update(status=status)
        messages.success(self.request, f'{n} pendaftar diubah menjadi {status}.')

    def bulk_verifikasi(self, ids):
        self._bulk_status(ids, 'verifikasi')

    def bulk_berkas_kurang(self, ids):
        self._bulk_status(ids, 'berkas_kurang')

    def bulk_tes(self, ids):
        self._bulk_status(ids, 'tes')

    def bulk_cadangan(self, ids):
        self._bulk_status(ids, 'cadangan')

    def bulk_ditolak(self, ids):
        self._bulk_status(ids, 'ditolak')


class DaftarGelombang(DaftarFilterMixin, OperasiMixin, ListView):
    model = GelombangPPDB
    template_name = 'ppdb/gelombang.html'
    context_object_name = 'daftar'
    search_fields = ('nama',)
    exact_filters = {'status': 'status'}
    date_field = 'mulai'
    export_filename = 'gelombang_ppdb.xlsx'
    export_columns = [
        ('Nama', 'nama'),
        ('Mulai', 'mulai'),
        ('Selesai', 'selesai'),
        ('Kuota', 'kuota'),
        ('Diterima', 'jumlah_diterima'),
        ('Status', 'get_status_display'),
    ]
    filter_fields = [
        {'name': 'status', 'label': 'Status', 'choices': GelombangPPDB.STATUS},
    ]
    aksi_massal_pilihan = [
        ('buka', 'Buka gelombang'),
        ('tutup', 'Tutup gelombang'),
    ]

    def bulk_buka(self, ids):
        n = GelombangPPDB.objects.filter(pk__in=ids).update(status=GelombangPPDB.DIBUKA)
        messages.success(self.request, f'{n} gelombang dibuka.')

    def bulk_tutup(self, ids):
        n = GelombangPPDB.objects.filter(pk__in=ids).update(status=GelombangPPDB.DITUTUP)
        messages.success(self.request, f'{n} gelombang ditutup.')


class TambahGelombang(OperasiMixin, CreateView):
    form_class = GelombangForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('ppdb:gelombang')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Gelombang PPDB'
        return ctx


class UbahGelombang(OperasiMixin, UpdateView):
    model = GelombangPPDB
    form_class = GelombangForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('ppdb:gelombang')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Ubah gelombang'
        return ctx


@butuh_operasi
def ubah_status(request, pk, status):
    if not (
        request.user.is_superuser
        or user_punya_grup(request.user, [GRUP_TU, 'mudir'])
    ):
        return HttpResponseForbidden('Hanya Tata Usaha yang mengubah status PPDB.')
    pendaftar = get_object_or_404(Pendaftaran, pk=pk)
    if status == 'diterima' and pendaftar.gelombang_id:
        gelombang = pendaftar.gelombang
        if gelombang and gelombang.sisa_kuota() <= 0 and pendaftar.status != 'diterima':
            pendaftar.status = 'cadangan'
            pendaftar.save(update_fields=['status'])
            messages.warning(
                request,
                f'Kuota {gelombang.nama} penuh. {pendaftar.nama_lengkap} masuk cadangan.',
            )
            return redirect('ppdb:antrian')
    pendaftar.status = status
    pendaftar.save(update_fields=['status'])
    if pendaftar.gelombang_id:
        pendaftar.gelombang.tutup_jika_kuota_penuh()
    if status == 'diterima':
        return redirect('ppdb:jadikan', pk=pk)
    messages.success(request, f'Status {pendaftar.nama_lengkap} diubah.')
    return redirect('ppdb:antrian')


@butuh_operasi
def jadikan_santri(request, pk):
    if not (
        request.user.is_superuser
        or user_punya_grup(request.user, [GRUP_TU, 'mudir'])
    ):
        return HttpResponseForbidden('Hanya Tata Usaha yang menjadikan santri.')
    pendaftar = get_object_or_404(Pendaftaran, pk=pk)
    rb_qs = RombonganBelajar.objects.select_related('ruang', 'tahun_ajaran')
    if pendaftar.gelombang_id and pendaftar.gelombang.unit_tujuan_id:
        rb_qs = rb_qs.filter(ruang__unit_id=pendaftar.gelombang.unit_tujuan_id)
    if request.method == 'POST':
        rb = rb_qs.filter(pk=request.POST.get('rb') or 0).first()
        kamar = Kamar.objects.filter(pk=request.POST.get('kamar') or 0).first()
        santri = terima_menjadi_santri(pendaftar, rb=rb, kamar=kamar)
        messages.success(request, f'{pendaftar.nama_lengkap} menjadi santri {santri.nomor_induk_santri}.')
        return redirect('ppdb:antrian')
    return render(request, 'ppdb/jadikan.html', {
        'pendaftar': pendaftar,
        'rb': rb_qs,
        'kamar': Kamar.objects.select_related('gedung'),
    })


@butuh_operasi
def status_gelombang(request, pk, status):
    if not (
        request.user.is_superuser
        or user_punya_grup(request.user, [GRUP_TU, 'mudir'])
    ):
        return HttpResponseForbidden('Hanya Tata Usaha yang mengubah gelombang.')
    gelombang = get_object_or_404(GelombangPPDB, pk=pk)
    gelombang.status = status
    gelombang.save(update_fields=['status'])
    messages.success(request, f'{gelombang.nama} sekarang {gelombang.get_status_display()}.')
    return redirect('ppdb:gelombang')


def cek_status(request):
    hasil = None
    pesan_berkas = ''
    if request.method == 'POST':
        kode = request.POST.get('kode', '').strip()
        tgl = request.POST.get('tanggal_lahir', '')
        qs = Pendaftaran.objects.filter(kode_pendaftaran__iexact=kode)
        if tgl:
            qs = qs.filter(tanggal_lahir=tgl)
        hasil = qs.first()
        if hasil and hasil.status == 'berkas_kurang' and request.FILES.get('foto'):
            hasil.foto = request.FILES['foto']
            hasil.status = 'dikirim'
            hasil.save()
            pesan_berkas = 'Berkas diunggah ulang. Status kembali ke dikirim untuk dicek Tata Usaha.'
            messages.success(request, pesan_berkas)
    return render(request, 'ppdb/cek_status.html', {'hasil': hasil, 'pesan_berkas': pesan_berkas})
