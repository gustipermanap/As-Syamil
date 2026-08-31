from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from akademik.models import RombonganBelajar
from pengguna.crud import UbahUmumMixin
from pengguna.daftar import DaftarFilterMixin
from pengguna.forms_util import kelas_bootstrap
from pengguna.mixins import KeuanganMixin, butuh_keuangan
from pengguna.notifikasi import catat_akses
from .models import JenisTagihan, Pembayaran, Tagihan
from .services import generate_tagihan_massal, terima_bayar


class JenisForm(forms.ModelForm):
    class Meta:
        model = JenisTagihan
        fields = ['nama', 'deskripsi']


class DaftarTagihan(DaftarFilterMixin, KeuanganMixin, ListView):
    model = Tagihan
    template_name = 'keuangan/tagihan_list.html'
    context_object_name = 'daftar'
    search_fields = ('santri__nama', 'santri__nomor_induk_santri', 'jenis__nama')
    exact_filters = {'status': 'status', 'jenis': 'jenis_id'}
    date_field = 'jatuh_tempo'
    cari_placeholder = 'Santri, NIS, jenis tagihan'
    export_filename = 'tagihan.xlsx'
    export_columns = [
        ('Santri', 'santri.nama'),
        ('NIS', 'santri.nomor_induk_santri'),
        ('Jenis', 'jenis.nama'),
        ('Jumlah', 'jumlah'),
        ('Potongan', 'potongan'),
        ('Sisa', 'sisa'),
        ('Status', 'get_status_display'),
        ('Jatuh tempo', 'jatuh_tempo'),
        ('Periode', 'periode'),
    ]
    aksi_massal_pilihan = [
        ('batal', 'Batalkan tagihan terpilih'),
    ]

    def get_filter_fields(self):
        return [
            {'name': 'status', 'label': 'Status', 'choices': Tagihan.STATUS},
            {
                'name': 'jenis',
                'label': 'Jenis',
                'choices': [(j.pk, j.nama) for j in JenisTagihan.objects.all()],
                'advanced': True,
            },
        ]

    def get_queryset(self):
        qs = Tagihan.objects.select_related('santri', 'jenis', 'periode').order_by('jatuh_tempo')
        if not self.request.GET.get('status'):
            qs = qs.exclude(status='batal')
        return self.apply_filters(qs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['jenis'] = JenisTagihan.objects.all()
        ctx['tunggakan'] = Tagihan.objects.exclude(status__in=['lunas', 'batal'])
        return ctx

    def bulk_batal(self, ids):
        n = Tagihan.objects.filter(pk__in=ids).exclude(status='lunas').update(status='batal')
        messages.success(self.request, f'{n} tagihan dibatalkan.')


class TambahJenis(KeuanganMixin, CreateView):
    form_class = JenisForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('keuangan:tagihan')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Jenis tagihan'
        return ctx


class UbahJenis(UbahUmumMixin, KeuanganMixin, UpdateView):
    model = JenisTagihan
    form_class = JenisForm
    success_url = reverse_lazy('keuangan:tagihan')
    judul = 'Ubah jenis tagihan'


class TagihanPotonganForm(forms.ModelForm):
    class Meta:
        model = Tagihan
        fields = ['potongan']


class UbahTagihan(UbahUmumMixin, KeuanganMixin, UpdateView):
    model = Tagihan
    form_class = TagihanPotonganForm
    success_url = reverse_lazy('keuangan:tagihan')
    judul = 'Potongan / beasiswa'

    def form_valid(self, form):
        try:
            form.instance.full_clean()
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        resp = super().form_valid(form)
        self.object.refresh_status()
        return resp


@butuh_keuangan
def generate(request):
    from lembaga.models import Periode
    if request.method == 'POST':
        jenis = get_object_or_404(JenisTagihan, pk=request.POST.get('jenis'))
        jumlah = request.POST.get('jumlah')
        jatuh = request.POST.get('jatuh_tempo')
        periode_id = request.POST.get('periode') or None
        rb_id = request.POST.get('rb') or None
        periode = Periode.objects.filter(pk=periode_id).first() if periode_id else None
        rb = RombonganBelajar.objects.filter(pk=rb_id).first() if rb_id else None
        dibuat = generate_tagihan_massal(jenis, jumlah, jatuh, periode=periode, rb=rb)
        messages.success(request, f'{len(dibuat)} tagihan dibuat.')
        return redirect('keuangan:tagihan')
    return render(request, 'keuangan/generate.html', {
        'jenis': JenisTagihan.objects.all(),
        'periode': Periode.objects.all(),
        'rb': RombonganBelajar.objects.all(),
    })


@butuh_keuangan
def bayar(request, pk):
    tagihan = get_object_or_404(Tagihan, pk=pk)
    error = ''
    if request.method == 'POST':
        try:
            jumlah = request.POST.get('jumlah')
            metode = request.POST.get('metode', 'tunai')
            bayaran = terima_bayar(tagihan, jumlah, request.user, metode=metode)
            messages.success(request, f'Pembayaran tercatat. Kwitansi {bayaran.nomor_kwitansi}.')
            return redirect('keuangan:kwitansi', pk=bayaran.pk)
        except ValidationError as exc:
            error = ' '.join(exc.messages) if hasattr(exc, 'messages') else str(exc)
            if hasattr(exc, 'message_dict'):
                error = ' '.join(str(v[0]) if isinstance(v, list) else str(v) for v in exc.message_dict.values())
    return render(request, 'keuangan/bayar.html', {'tagihan': tagihan, 'error': error})


@butuh_keuangan
def kwitansi(request, pk):
    bayaran = get_object_or_404(Pembayaran, pk=pk)
    catat_akses(request.user, 'lihat_kwitansi', objek=bayaran.nomor_kwitansi, ringkas='kwitansi')
    return render(request, 'keuangan/kwitansi.html', {'bayaran': bayaran})
