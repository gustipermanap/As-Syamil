from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from pengguna.forms_util import kelas_bootstrap
from pengguna.mixins import OperasiMixin
from pengguna.models import GRUP_MUDIR, GRUP_TU
from pengguna.services import user_punya_grup
from .models import Jenjang, Pengaturan, Periode, TahunAjaran, UnitPendidikan


class PengaturanForm(forms.ModelForm):
    class Meta:
        model = Pengaturan
        fields = [
            'nama_tampil', 'nsm', 'npsn', 'pengelola_keuangan', 'portal_santri_aktif',
            'jenis_periode', 'modul_ppdb', 'modul_akademik', 'modul_tahfidz',
            'modul_asrama', 'modul_keuangan', 'modul_kedisiplinan',
            'predikat_a', 'predikat_b', 'predikat_c', 'predikat_d', 'ambang_alpa',
        ]


class UnitForm(forms.ModelForm):
    class Meta:
        model = UnitPendidikan
        fields = ['nama', 'tipe', 'aktif', 'label_peserta']


class JenjangForm(forms.ModelForm):
    class Meta:
        model = Jenjang
        fields = ['unit', 'nama', 'urutan']


class TahunAjaranForm(forms.ModelForm):
    class Meta:
        model = TahunAjaran
        fields = ['nama', 'mulai', 'selesai', 'aktif']
        widgets = {
            'mulai': forms.DateInput(attrs={'type': 'date'}),
            'selesai': forms.DateInput(attrs={'type': 'date'}),
        }


class PeriodeForm(forms.ModelForm):
    class Meta:
        model = Periode
        fields = ['tahun_ajaran', 'nama', 'mulai', 'selesai', 'aktif']
        widgets = {
            'mulai': forms.DateInput(attrs={'type': 'date'}),
            'selesai': forms.DateInput(attrs={'type': 'date'}),
        }


def _boleh_ubah(user):
    return user.is_superuser or user_punya_grup(user, [GRUP_TU, GRUP_MUDIR])


class UbahPengaturan(OperasiMixin, UpdateView):
    model = Pengaturan
    form_class = PengaturanForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('lembaga:pengaturan')

    def get_object(self, queryset=None):
        return Pengaturan.get()

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Pengaturan lembaga'
        ctx['submit_label'] = 'Simpan pengaturan'
        return ctx

    def form_valid(self, form):
        if not _boleh_ubah(self.request.user):
            messages.error(self.request, 'Hanya mudir atau Tata Usaha yang mengubah pengaturan.')
            return redirect('lembaga:pengaturan')
        messages.success(self.request, 'Pengaturan disimpan.')
        return super().form_valid(form)


class DaftarUnit(OperasiMixin, ListView):
    model = UnitPendidikan
    template_name = 'lembaga/unit_list.html'
    context_object_name = 'daftar'


class TambahUnit(OperasiMixin, CreateView):
    model = UnitPendidikan
    form_class = UnitForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('lembaga:unit')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Unit pendidikan baru'
        return ctx


class TambahJenjang(OperasiMixin, CreateView):
    model = Jenjang
    form_class = JenjangForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('lembaga:unit')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Jenjang baru'
        return ctx


class DaftarTahunAjaran(OperasiMixin, ListView):
    model = TahunAjaran
    template_name = 'lembaga/tahun_list.html'
    context_object_name = 'daftar'


class TambahTahunAjaran(OperasiMixin, CreateView):
    model = TahunAjaran
    form_class = TahunAjaranForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('lembaga:tahun')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Tahun ajaran'
        return ctx


class TambahPeriode(OperasiMixin, CreateView):
    model = Periode
    form_class = PeriodeForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('lembaga:tahun')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Periode'
        return ctx
