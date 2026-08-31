from datetime import date, timedelta

from django import forms
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from pengguna.daftar import DaftarFilterMixin
from pengguna.forms_util import kelas_bootstrap
from pengguna.mixins import OperasiMixin
from .models import ProgressHafalan, SetoranHafalan
from .services import catat_setoran


class SetoranForm(forms.ModelForm):
    class Meta:
        model = SetoranHafalan
        fields = [
            'santri', 'jenis', 'dari_juz', 'dari_halaman', 'sampai_juz',
            'sampai_halaman', 'mutu', 'catatan_tajwid', 'penyimak', 'tanggal',
        ]
        widgets = {'tanggal': forms.DateInput(attrs={'type': 'date'})}


class DaftarSetoran(DaftarFilterMixin, OperasiMixin, ListView):
    model = SetoranHafalan
    template_name = 'tahfidz/setoran_list.html'
    context_object_name = 'daftar'
    search_fields = ('santri__nama', 'santri__nomor_induk_santri', 'catatan_tajwid', 'penyimak__nama')
    exact_filters = {'jenis': 'jenis', 'mutu': 'mutu'}
    date_field = 'tanggal'
    cari_placeholder = 'Santri, NIS, penyimak'
    export_filename = 'setoran.xlsx'
    export_columns = [
        ('Tanggal', 'tanggal'),
        ('Santri', 'santri.nama'),
        ('Jenis', 'get_jenis_display'),
        ('Mutu', 'get_mutu_display'),
        ('Dari juz', 'dari_juz'),
        ('Dari halaman', 'dari_halaman'),
        ('Sampai juz', 'sampai_juz'),
        ('Sampai halaman', 'sampai_halaman'),
        ('Penyimak', 'penyimak.nama'),
    ]
    filter_fields = [
        {'name': 'jenis', 'label': 'Jenis', 'choices': SetoranHafalan.JENIS},
        {'name': 'mutu', 'label': 'Mutu', 'choices': SetoranHafalan.MUTU, 'advanced': True},
    ]

    def get_queryset(self):
        return super().get_queryset().select_related('santri', 'penyimak').order_by('-tanggal', '-id')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['progress'] = ProgressHafalan.objects.select_related('santri')
        minggu = date.today() - timedelta(days=7)
        ctx['setoran_minggu'] = (
            SetoranHafalan.objects.filter(tanggal__gte=minggu)
            .values('santri__nama')
            .annotate(jumlah=Count('id'))
        )
        return ctx


class TambahSetoran(OperasiMixin, CreateView):
    form_class = SetoranForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('tahfidz:setoran')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Catat setoran hafalan'
        return ctx
