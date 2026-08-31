from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from pengguna.daftar import DaftarFilterMixin
from pengguna.forms_util import kelas_bootstrap
from pengguna.mixins import OperasiMixin, butuh_operasi, butuh_santri, butuh_wali
from .models import (
    AbsensiAsrama, CatatanPelanggaran, Gedung, Izin, JenisPelanggaran, Kamar,
    Pegawai, PenempatanKamar, Santri, WaliSantri,
)
from pengguna.notifikasi import catat_akses
from .services import anak_wali, pindah_kamar, proses_izin, santri_portal, tautkan_akun_pegawai, tautkan_akun_santri, tautkan_akun_wali


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username
            self.fields['username'].help_text = 'Sudah tertaut. Isi sandi hanya jika ingin mengganti.'
            grup = self.instance.user.groups.first()
            if grup:
                self.fields['grup'].initial = grup.name


class SantriForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        help_text='Untuk portal santri. Kosongkan jika belum perlu akun.',
    )
    sandi = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Santri
        fields = [
            'nomor_induk_santri', 'nisn', 'nama', 'nik', 'tempat_lahir', 'tanggal_lahir',
            'jenis_kelamin', 'status', 'wali', 'foto', 'alamat',
        ]
        widgets = {'tanggal_lahir': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username
            self.fields['username'].help_text = 'Sudah tertaut. Isi sandi hanya jika ingin mengganti.'


class WaliForm(forms.ModelForm):
    username = forms.CharField(required=False, help_text='Untuk portal wali. Kosongkan jika belum perlu akun.')
    sandi = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = WaliSantri
        fields = ['nama', 'hubungan', 'kontak', 'alamat', 'pekerjaan']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username
            self.fields['username'].help_text = 'Sudah tertaut. Isi sandi hanya jika ingin mengganti.'


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


class DaftarSantri(DaftarFilterMixin, OperasiMixin, ListView):
    model = Santri
    template_name = 'kesiswaan/santri_list.html'
    context_object_name = 'daftar'
    search_fields = ('nama', 'nomor_induk_santri', 'nisn', 'nik')
    exact_filters = {'status': 'status', 'jenis_kelamin': 'jenis_kelamin'}
    date_field = 'tanggal_lahir'
    cari_placeholder = 'Nama, NIS, NISN, NIK'
    export_filename = 'santri.xlsx'
    export_columns = [
        ('NIS', 'nomor_induk_santri'),
        ('Nama', 'nama'),
        ('JK', 'get_jenis_kelamin_display'),
        ('Status', 'get_status_display'),
        ('Wali', 'wali.nama'),
        ('Tanggal lahir', 'tanggal_lahir'),
        ('NISN', 'nisn'),
    ]
    filter_fields = [
        {'name': 'status', 'label': 'Status', 'choices': Santri.STATUS},
        {'name': 'jenis_kelamin', 'label': 'Jenis kelamin', 'choices': Santri.JENIS_KELAMIN, 'advanced': True},
    ]
    aksi_massal_pilihan = [
        ('aktif', 'Ubah status: Aktif'),
        ('lulus', 'Ubah status: Lulus'),
        ('keluar', 'Ubah status: Keluar'),
        ('izin_panjang', 'Ubah status: Izin panjang'),
    ]

    def get_queryset(self):
        return super().get_queryset().select_related('wali').order_by('nama')

    def _bulk_status(self, ids, status):
        n = Santri.objects.filter(pk__in=ids).update(status=status)
        messages.success(self.request, f'{n} santri diubah menjadi {status}.')

    def bulk_aktif(self, ids):
        self._bulk_status(ids, 'aktif')

    def bulk_lulus(self, ids):
        self._bulk_status(ids, 'lulus')

    def bulk_keluar(self, ids):
        self._bulk_status(ids, 'keluar')

    def bulk_izin_panjang(self, ids):
        self._bulk_status(ids, 'izin_panjang')


class DetailSantri(OperasiMixin, DetailView):
    model = Santri
    template_name = 'kesiswaan/santri_detail.html'
    context_object_name = 'santri'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pelanggaran'] = self.object.pelanggaran.select_related('jenis')
        ctx['poin'] = sum(p.jenis.poin for p in ctx['pelanggaran'])
        ctx['kamar'] = self.object.penempatan_kamar.filter(keluar__isnull=True).select_related('kamar__gedung').first()
        ctx['riwayat_kamar'] = self.object.penempatan_kamar.select_related('kamar__gedung').order_by('-masuk')
        ctx['rb'] = self.object.keanggotaan_rb.select_related('rb')
        catat_akses(self.request.user, 'lihat_santri', objek=self.object.nomor_induk_santri, ringkas='profil')
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
        ctx['deskripsi'] = 'Tautkan akun portal santri di sini jika belum punya login.'
        return ctx

    def form_valid(self, form):
        santri = form.save()
        try:
            tautkan_akun_santri(
                santri,
                form.cleaned_data.get('username'),
                form.cleaned_data.get('sandi'),
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        messages.success(self.request, 'Santri disimpan.')
        return redirect(self.get_success_url())


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

    def form_valid(self, form):
        santri = form.save()
        try:
            tautkan_akun_santri(
                santri,
                form.cleaned_data.get('username'),
                form.cleaned_data.get('sandi'),
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        messages.success(self.request, 'Santri disimpan.')
        return redirect(self.success_url)


class DaftarPegawai(DaftarFilterMixin, OperasiMixin, ListView):
    model = Pegawai
    template_name = 'kesiswaan/pegawai_list.html'
    context_object_name = 'daftar'
    search_fields = ('nama', 'kontak', 'user__username')
    boolean_filters = {'aktif': 'aktif'}
    exact_filters = {'jenis_kelamin': 'jenis_kelamin'}
    cari_placeholder = 'Nama, kontak, akun'
    export_filename = 'pegawai.xlsx'
    export_columns = [
        ('Nama', 'nama'),
        ('JK', 'get_jenis_kelamin_display'),
        ('Aktif', 'aktif'),
        ('Akun', 'user.username'),
        ('Kontak', 'kontak'),
    ]
    filter_fields = [
        {'name': 'aktif', 'label': 'Status', 'choices': [('1', 'Aktif'), ('0', 'Nonaktif')]},
        {'name': 'jenis_kelamin', 'label': 'Jenis kelamin', 'choices': Pegawai.JENIS_KELAMIN, 'advanced': True},
    ]
    aksi_massal_pilihan = [
        ('aktifkan', 'Aktifkan'),
        ('nonaktifkan', 'Nonaktifkan'),
    ]

    def get_queryset(self):
        return super().get_queryset().select_related('user').order_by('nama')

    def bulk_aktifkan(self, ids):
        n = 0
        for p in Pegawai.objects.filter(pk__in=ids):
            p.aktif = True
            p.save()
            n += 1
        messages.success(self.request, f'{n} pegawai diaktifkan.')

    def bulk_nonaktifkan(self, ids):
        n = 0
        for p in Pegawai.objects.filter(pk__in=ids):
            p.aktif = False
            p.save()
            n += 1
        messages.success(self.request, f'{n} pegawai dinonaktifkan.')


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
        try:
            tautkan_akun_pegawai(
                pegawai,
                form.cleaned_data.get('username'),
                form.cleaned_data.get('sandi'),
                form.cleaned_data.get('grup'),
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        messages.success(self.request, 'Pegawai disimpan.')
        return redirect(self.success_url)


class UbahPegawai(OperasiMixin, UpdateView):
    model = Pegawai
    form_class = PegawaiForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:pegawai')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = f'Ubah {self.object.nama}'
        ctx['deskripsi'] = 'Tautkan atau ganti akun staf di sini jika pegawai belum punya login.'
        return ctx

    def form_valid(self, form):
        pegawai = form.save()
        try:
            tautkan_akun_pegawai(
                pegawai,
                form.cleaned_data.get('username'),
                form.cleaned_data.get('sandi'),
                form.cleaned_data.get('grup'),
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
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

    def form_valid(self, form):
        wali = form.save()
        try:
            tautkan_akun_wali(wali, form.cleaned_data.get('username'), form.cleaned_data.get('sandi'))
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        messages.success(self.request, 'Wali disimpan.')
        return redirect(self.success_url)


class UbahWali(OperasiMixin, UpdateView):
    model = WaliSantri
    form_class = WaliForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:santri')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = f'Ubah wali {self.object.nama}'
        return ctx

    def form_valid(self, form):
        wali = form.save()
        try:
            tautkan_akun_wali(wali, form.cleaned_data.get('username'), form.cleaned_data.get('sandi'))
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        messages.success(self.request, 'Wali disimpan.')
        return redirect(self.success_url)


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


class UbahGedung(OperasiMixin, UpdateView):
    model = Gedung
    form_class = GedungForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:asrama')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = f'Ubah gedung {self.object.nama}'
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


class UbahKamar(OperasiMixin, UpdateView):
    model = Kamar
    form_class = KamarForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('kesiswaan:asrama')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = f'Ubah kamar {self.object}'
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


class DaftarIzin(DaftarFilterMixin, OperasiMixin, ListView):
    model = Izin
    template_name = 'kesiswaan/izin_list.html'
    context_object_name = 'daftar'
    search_fields = ('santri__nama', 'santri__nomor_induk_santri', 'alasan')
    exact_filters = {'status': 'status', 'jenis': 'jenis'}
    date_field = 'mulai'
    cari_placeholder = 'Nama santri, NIS, alasan'
    export_filename = 'izin.xlsx'
    export_columns = [
        ('Santri', 'santri.nama'),
        ('NIS', 'santri.nomor_induk_santri'),
        ('Jenis', 'get_jenis_display'),
        ('Status', 'get_status_display'),
        ('Mulai', 'mulai'),
        ('Selesai', 'selesai'),
        ('Alasan', 'alasan'),
    ]
    filter_fields = [
        {'name': 'status', 'label': 'Status', 'choices': Izin.STATUS},
        {'name': 'jenis', 'label': 'Jenis', 'choices': Izin.JENIS, 'advanced': True},
    ]
    aksi_massal_pilihan = [
        ('setujui', 'Setujui'),
        ('tolak', 'Tolak'),
    ]

    def get_queryset(self):
        return super().get_queryset().select_related('santri').order_by('-mulai')

    def bulk_setujui(self, ids):
        n = 0
        for izin in Izin.objects.filter(pk__in=ids, status='diajukan'):
            proses_izin(izin, 'setujui')
            n += 1
        messages.success(self.request, f'{n} izin disetujui.')

    def bulk_tolak(self, ids):
        n = 0
        for izin in Izin.objects.filter(pk__in=ids, status='diajukan'):
            proses_izin(izin, 'tolak')
            n += 1
        messages.success(self.request, f'{n} izin ditolak.')


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


class DaftarPelanggaran(DaftarFilterMixin, OperasiMixin, ListView):
    model = CatatanPelanggaran
    template_name = 'kesiswaan/pelanggaran_list.html'
    context_object_name = 'daftar'
    search_fields = ('santri__nama', 'santri__nomor_induk_santri', 'jenis__nama', 'sanksi')
    exact_filters = {'kategori': 'jenis__kategori'}
    date_field = 'tanggal'
    cari_placeholder = 'Santri, jenis, sanksi'
    export_filename = 'pelanggaran.xlsx'
    export_columns = [
        ('Tanggal', 'tanggal'),
        ('Santri', 'santri.nama'),
        ('Jenis', 'jenis.nama'),
        ('Kategori', 'jenis.get_kategori_display'),
        ('Poin', 'jenis.poin'),
        ('Sanksi', 'sanksi'),
    ]
    filter_fields = [
        {'name': 'kategori', 'label': 'Kategori', 'choices': JenisPelanggaran._meta.get_field('kategori').choices},
    ]

    def get_queryset(self):
        return super().get_queryset().select_related('santri', 'jenis').order_by('-tanggal')


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


@butuh_santri
def izin_santri(request):
    santri = santri_portal(request.user)
    if not santri:
        messages.error(request, 'Akun ini belum tertaut ke data santri.')
        return redirect('pengguna:santri')
    if request.method == 'POST':
        form = kelas_bootstrap(IzinForm(request.POST))
        form.fields.pop('santri')
        if form.is_valid():
            izin = form.save(commit=False)
            izin.santri = santri
            izin.pemohon = request.user
            izin.save()
            messages.success(request, 'Izin diajukan. Menunggu persetujuan pengasuhan.')
            return redirect('pengguna:santri')
    else:
        form = kelas_bootstrap(IzinForm())
        form.fields.pop('santri')
    return render(request, 'pengguna/form_umum.html', {
        'judul': f'Ajukan izin — {santri.nama}',
        'form': form,
    })


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


@butuh_operasi
def absensi_asrama(request):
    from datetime import date
    tanggal = request.POST.get('tanggal') or request.GET.get('tanggal') or date.today().isoformat()
    sesi = request.POST.get('sesi') or request.GET.get('sesi') or 'malam'
    santri_asrama = Santri.objects.filter(
        status='aktif',
        pk__in=PenempatanKamar.objects.filter(keluar__isnull=True).values('santri'),
    ).distinct().order_by('nama')
    if request.method == 'POST':
        for s in santri_asrama:
            status = request.POST.get(f'status_{s.pk}', 'hadir')
            AbsensiAsrama.objects.update_or_create(
                santri=s, tanggal=tanggal, sesi=sesi,
                defaults={'status': status, 'petugas': getattr(request.user, 'pegawai', None)},
            )
        messages.success(request, 'Absensi asrama disimpan.')
        return redirect(f"{reverse('kesiswaan:absensi_asrama')}?tanggal={tanggal}&sesi={sesi}")
    tersimpan = {
        a.santri_id: a.status
        for a in AbsensiAsrama.objects.filter(tanggal=tanggal, sesi=sesi)
    }
    baris = [{'santri': s, 'status': tersimpan.get(s.pk, 'hadir')} for s in santri_asrama]
    return render(request, 'kesiswaan/absensi_asrama.html', {
        'tanggal': tanggal,
        'sesi': sesi,
        'baris': baris,
        'pilihan': AbsensiAsrama.STATUS,
        'sesi_pilihan': AbsensiAsrama.SESI,
    })


@butuh_operasi
def pindah_kamar_view(request):
    from datetime import date
    if request.method == 'POST':
        santri = get_object_or_404(Santri, pk=request.POST.get('santri'))
        kamar = get_object_or_404(Kamar, pk=request.POST.get('kamar'))
        try:
            pindah_kamar(santri, kamar, date.today())
            messages.success(request, f'{santri.nama} dipindah ke {kamar}.')
            return redirect('kesiswaan:asrama')
        except ValidationError as exc:
            messages.error(request, ' '.join(exc.messages) if hasattr(exc, 'messages') else str(exc))
    return render(request, 'pengguna/form_umum.html', {
        'judul': 'Pindah kamar',
        'form_html': (
            '<div class="mb-3"><label class="form-label">Santri</label>'
            '<select class="form-control" name="santri">'
            + ''.join(
                f'<option value="{s.pk}">{s.nama}</option>'
                for s in Santri.objects.filter(status='aktif')
            )
            + '</select></div>'
            '<div class="mb-3"><label class="form-label">Kamar baru</label>'
            '<select class="form-control" name="kamar">'
            + ''.join(f'<option value="{k.pk}">{k}</option>' for k in Kamar.objects.select_related('gedung'))
            + '</select></div>'
        ),
        'submit_label': 'Pindahkan',
    })
