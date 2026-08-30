from django import forms
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from pengguna.forms_util import kelas_bootstrap
from pengguna.mixins import OperasiMixin, WaliMixin, butuh_operasi, butuh_wali
from pengguna.models import GRUP_SANTRI, GRUP_WALI
from .models import (
    CatatanPelanggaran, Gedung, Izin, JenisPelanggaran, Kamar,
    Pegawai, PenempatanKamar, Santri, WaliSantri,
)
from .services import anak_wali, proses_izin, santri_portal


class PegawaiForm(forms.ModelForm):
    username = forms.CharField(required=False)
    sandi = forms.CharField(required=False, widget=forms.PasswordInput)
    grup = forms.ChoiceField(
        required=False,
        choices=[('', '—')] + [
            ('ustadz', 'Ustadz'), ('musyrif', 'Musyrif'),
            ('tata_usaha', 'Tata Usaha'), ('bendahara', 'Bendahara'), ('mudir', 'Mudir'),
        ],
    )

    class Meta:
        model = Pegawai
        fields = ['nama', 'jenis_kelamin', 'kontak', 'aktif']


class SantriForm(forms.ModelForm):
    class Meta:
        model = Santri
        fields = [
            'nomor_induk_santri', 'nisn', 'nama', 'nik', 'tempat_lahir', 'tanggal_lahir',
            'jenis_kelamin', 'status', 'wali', 'foto', 'alamat',
        ]
        widgets = {'tanggal_lahir': forms.DateInput(attrs={'type': 'date'})}


class WaliForm(forms.ModelForm):
    class Meta:
        model = WaliSantri
        fields = ['nama', 'hubungan', 'kontak', 'alamat', 'pekerjaan']


class GedungForm(forms.ModelForm):
    class Meta:
        model = Gedung
        fields = ['nama', 'putra_putri']


class KamarForm(forms.ModelForm):
    class Meta:
        model = Kamar
        fields = ['gedung', 'nama', 'kapasitas']


class PenempatanForm(forms.ModelForm):
    class Meta:
        model = PenempatanKamar
        fields = ['santri', 'kamar', 'masuk', 'keluar']
        widgets = {
            'masuk': forms.DateInput(attrs={'type': 'date'}),
            'keluar': forms.DateInput(attrs={'type': 'date'}),
        }


class IzinForm(forms.ModelForm):
    class Meta:
        model = Izin
        fields = ['santri', 'jenis', 'mulai', 'selesai', 'alasan']
        widgets = {
            'mulai': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'selesai': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class PelanggaranForm(forms.ModelForm):
    class Meta:
        model = CatatanPelanggaran
        fields = ['santri', 'jenis', 'tanggal', 'sanksi', 'catatan']
        widgets = {'tanggal': forms.DateInput(attrs={'type': 'date'})}


class JenisPelanggaranForm(forms.ModelForm):
    class Meta:
        model = JenisPelanggaran
        fields = ['nama', 'poin', 'kategori']


class DaftarSantri(OperasiMixin, ListView):
    model = Santri
    template_name = 'kesiswaan/santri_list.html'
    context_object_name = 'daftar'
    paginate_by = 50

    def get_queryset(self):
        qs = Santri.objects.select_related('wali').order_by('nama')
        status = self.request.GET.get('status')
        q = self.request.GET.get('q')
        if status:
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(nama__icontains=q)
        return qs


class DetailSantri(OperasiMixin, DetailView):
    model = Santri
    template_name = 'kesiswaan/santri_detail.html'
    context_object_name = 'santri'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pelanggaran'] = self.object.pelanggaran.select_related('jenis')
        ctx['poin'] = sum(p.jenis.poin for p in ctx['pelanggaran'])
        ctx['kamar'] = self.object.penempatan_kamar.filter(keluar__isnull=True).select_related('kamar__gedung').first()
        ctx['rb'] = self.object.keanggotaan_rb.select_related('rb')
        return ctx


class UbahSantri(OperasiMixin, UpdateView):
    model = Santri
    form_class = SantriForm
    template_name = 'pengguna/form_umum.html'

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_success_url(self):
        return reverse_lazy('kesiswaan:santri_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = f'Ubah {self.object.nama}'
        ctx['enctype'] = 'multipart/form-data'
        return ctx


class TambahSantri(OperasiMixin, CreateView):
    model = Santri
    form_class = SantriForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:santri')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Santri baru'
        ctx['enctype'] = 'multipart/form-data'
        return ctx


class DaftarPegawai(OperasiMixin, ListView):
    model = Pegawai
    template_name = 'kesiswaan/pegawai_list.html'
    context_object_name = 'daftar'


class TambahPegawai(OperasiMixin, CreateView):
    form_class = PegawaiForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:pegawai')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Pegawai baru'
        return ctx

    def form_valid(self, form):
        pegawai = form.save()
        username = form.cleaned_data.get('username')
        sandi = form.cleaned_data.get('sandi')
        grup = form.cleaned_data.get('grup')
        if username and sandi:
            user = User.objects.create_user(username=username, password=sandi)
            pegawai.user = user
            pegawai.save()
            if grup:
                g, _ = Group.objects.get_or_create(name=grup)
                user.groups.add(g)
        messages.success(self.request, 'Pegawai disimpan.')
        return redirect(self.success_url)


@butuh_operasi
def nonaktifkan_pegawai(request, pk):
    pegawai = get_object_or_404(Pegawai, pk=pk)
    pegawai.aktif = not pegawai.aktif
    pegawai.save()
    messages.success(request, f'{pegawai.nama} sekarang {"aktif" if pegawai.aktif else "nonaktif"}.')
    return redirect('kesiswaan:pegawai')


class TambahWali(OperasiMixin, CreateView):
    form_class = WaliForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:santri')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Wali santri baru'
        return ctx


class AsramaDasbor(OperasiMixin, ListView):
    model = Kamar
    template_name = 'kesiswaan/asrama.html'
    context_object_name = 'kamar'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['gedung'] = Gedung.objects.all()
        ctx['penempatan'] = PenempatanKamar.objects.filter(keluar__isnull=True).select_related(
            'santri', 'kamar__gedung',
        )
        return ctx


class TambahGedung(OperasiMixin, CreateView):
    form_class = GedungForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:asrama')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Gedung baru'
        return ctx


class TambahKamar(OperasiMixin, CreateView):
    form_class = KamarForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:asrama')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Kamar baru'
        return ctx


class TambahPenempatan(OperasiMixin, CreateView):
    form_class = PenempatanForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:asrama')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Penempatan kamar'
        return ctx

    def form_valid(self, form):
        try:
            form.save()
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        messages.success(self.request, 'Penempatan disimpan.')
        return redirect(self.success_url)


class DaftarIzin(OperasiMixin, ListView):
    model = Izin
    template_name = 'kesiswaan/izin_list.html'
    context_object_name = 'daftar'

    def get_queryset(self):
        return Izin.objects.select_related('santri').order_by('-mulai')


class TambahIzin(OperasiMixin, CreateView):
    form_class = IzinForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:izin')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def form_valid(self, form):
        izin = form.save(commit=False)
        izin.pemohon = self.request.user
        izin.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Ajukan izin'
        return ctx


@butuh_operasi
def aksi_izin(request, pk, aksi):
    izin = get_object_or_404(Izin, pk=pk)
    try:
        proses_izin(izin, aksi)
        messages.success(request, f'Izin {izin.santri.nama} sekarang {izin.get_status_display()}.')
    except ValidationError as exc:
        messages.error(request, ' '.join(exc.messages))
    return redirect('kesiswaan:izin')


class DaftarPelanggaran(OperasiMixin, ListView):
    model = CatatanPelanggaran
    template_name = 'kesiswaan/pelanggaran_list.html'
    context_object_name = 'daftar'

    def get_queryset(self):
        return CatatanPelanggaran.objects.select_related('santri', 'jenis').order_by('-tanggal')


class TambahPelanggaran(OperasiMixin, CreateView):
    form_class = PelanggaranForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:pelanggaran')

    def get_form(self, form_class=None):
        form = kelas_bootstrap(super().get_form(form_class))
        form.instance.pelapor = getattr(self.request.user, 'pegawai', None)
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Catat pelanggaran'
        return ctx


class TambahJenisPelanggaran(OperasiMixin, CreateView):
    form_class = JenisPelanggaranForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:pelanggaran')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Jenis pelanggaran'
        return ctx


@butuh_wali
def izin_wali(request):
    anak = anak_wali(request.user)
    if request.method == 'POST':
        form = kelas_bootstrap(IzinForm(request.POST))
        form.fields['santri'].queryset = anak
        if form.is_valid():
            izin = form.save(commit=False)
            izin.pemohon = request.user
            izin.save()
            messages.success(request, 'Izin diajukan.')
            return redirect('pengguna:wali')
    else:
        form = kelas_bootstrap(IzinForm())
        form.fields['santri'].queryset = anak
    return render(request, 'pengguna/form_umum.html', {'judul': 'Ajukan izin anak', 'form': form})
