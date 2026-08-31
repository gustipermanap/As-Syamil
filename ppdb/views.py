from django import forms
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from akademik.models import RombonganBelajar
from kesiswaan.models import Kamar
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


class AntrianPPDB(OperasiMixin, ListView):
    model = Pendaftaran
    template_name = 'ppdb/antrian.html'
    context_object_name = 'daftar'
    paginate_by = 50

    def get_queryset(self):
        qs = Pendaftaran.objects.select_related('gelombang').order_by('-id')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs


class DaftarGelombang(OperasiMixin, ListView):
    model = GelombangPPDB
    template_name = 'ppdb/gelombang.html'
    context_object_name = 'daftar'


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
    pendaftar.status = status
    pendaftar.save(update_fields=['status'])
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
    if request.method == 'POST':
        rb = RombonganBelajar.objects.filter(pk=request.POST.get('rb') or 0).first()
        kamar = Kamar.objects.filter(pk=request.POST.get('kamar') or 0).first()
        santri = terima_menjadi_santri(pendaftar, rb=rb, kamar=kamar)
        messages.success(request, f'{pendaftar.nama_lengkap} menjadi santri {santri.nomor_induk_santri}.')
        return redirect('ppdb:antrian')
    return render(request, 'ppdb/jadikan.html', {
        'pendaftar': pendaftar,
        'rb': RombonganBelajar.objects.select_related('ruang', 'tahun_ajaran'),
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
    if request.method == 'POST':
        kode = request.POST.get('kode', '').strip()
        tgl = request.POST.get('tanggal_lahir', '')
        qs = Pendaftaran.objects.filter(kode_pendaftaran__iexact=kode)
        if tgl:
            qs = qs.filter(tanggal_lahir=tgl)
        hasil = qs.first()
    return render(request, 'ppdb/cek_status.html', {'hasil': hasil})
