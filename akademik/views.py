from datetime import date

from django import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from kesiswaan.models import Pegawai, Santri
from lembaga.models import Pengaturan, TahunAjaran
from pengguna.daftar import DaftarFilterMixin
from pengguna.forms_util import kelas_bootstrap
from pengguna.mixins import OperasiMixin, butuh_operasi
from pengguna.models import GRUP_TU, GRUP_USTADZ
from pengguna.services import user_punya_grup
from .models import (
    Absensi, JadwalSlot, KeanggotaanRB, KitabAtauMapel, MapelRB,
    Penilaian, PengampuRB, Pertemuan, RombonganBelajar, RuangBelajar,
)
from .services import queryset_rekap_absensi, salin_rb, streak_alpa


class RuangForm(forms.ModelForm):
    class Meta:
        model = RuangBelajar
        fields = ['unit', 'jenjang', 'nama', 'tipe']


class RBForm(forms.ModelForm):
    class Meta:
        model = RombonganBelajar
        fields = ['ruang', 'tahun_ajaran', 'nama']


class MapelForm(forms.ModelForm):
    class Meta:
        model = KitabAtauMapel
        fields = ['unit', 'jenjang', 'nama', 'jenis', 'kkm']


class JadwalForm(forms.ModelForm):
    class Meta:
        model = JadwalSlot
        fields = ['rb', 'hari', 'jam_mulai', 'jam_selesai', 'mapel', 'pengampu']
        widgets = {
            'jam_mulai': forms.TimeInput(attrs={'type': 'time'}),
            'jam_selesai': forms.TimeInput(attrs={'type': 'time'}),
        }


class PertemuanForm(forms.ModelForm):
    class Meta:
        model = Pertemuan
        fields = ['rb', 'mapel', 'pengampu', 'tanggal', 'catatan']
        widgets = {'tanggal': forms.DateInput(attrs={'type': 'date'})}


class NilaiForm(forms.ModelForm):
    class Meta:
        model = Penilaian
        fields = ['santri', 'mapel', 'rb', 'periode', 'jenis', 'nilai']


def _pegawai(user):
    return getattr(user, 'pegawai', None)


def _hanya_ampuan(user, qs):
    if user_punya_grup(user, [GRUP_TU, 'mudir']) or user.is_superuser:
        return qs
    pegawai = _pegawai(user)
    if not pegawai:
        return qs.none()
    rb_ids = list(PengampuRB.objects.filter(pegawai=pegawai).values_list('rb_id', flat=True))
    rb_ids += list(JadwalSlot.objects.filter(pengampu=pegawai).values_list('rb_id', flat=True))
    return qs.filter(pk__in=rb_ids)


class DaftarRB(DaftarFilterMixin, OperasiMixin, ListView):
    model = RombonganBelajar
    template_name = 'akademik/rb_list.html'
    context_object_name = 'daftar'
    search_fields = ('nama', 'ruang__nama', 'tahun_ajaran__nama')
    exact_filters = {'tahun': 'tahun_ajaran_id', 'tipe': 'ruang__tipe'}
    cari_placeholder = 'Nama RB, ruang, tahun ajaran'
    export_filename = 'rombongan_belajar.xlsx'
    export_columns = [
        ('Nama', 'nama'),
        ('Ruang', 'ruang.nama'),
        ('Tipe', 'ruang.get_tipe_display'),
        ('Tahun ajaran', 'tahun_ajaran.nama'),
        ('Unit', 'ruang.unit.nama'),
    ]

    def get_filter_fields(self):
        return [
            {
                'name': 'tahun',
                'label': 'Tahun ajaran',
                'choices': [(t.pk, t.nama) for t in TahunAjaran.objects.all()],
            },
            {'name': 'tipe', 'label': 'Tipe ruang', 'choices': RuangBelajar.TIPE, 'advanced': True},
        ]

    def get_queryset(self):
        qs = _hanya_ampuan(
            self.request.user,
            RombonganBelajar.objects.select_related('ruang', 'tahun_ajaran', 'ruang__unit'),
        )
        return self.apply_filters(qs)


class DetailRB(OperasiMixin, DetailView):
    model = RombonganBelajar
    template_name = 'akademik/rb_detail.html'
    context_object_name = 'rb'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['anggota'] = self.object.anggota.select_related('santri')
        ctx['pengampu'] = self.object.pengampu.select_related('pegawai')
        ctx['mapel'] = self.object.mapel_rb.select_related('mapel')
        ctx['jadwal'] = self.object.jadwal.select_related('mapel', 'pengampu')
        ctx['tahun_lain'] = TahunAjaran.objects.exclude(pk=self.object.tahun_ajaran_id)
        return ctx


class TambahRuang(OperasiMixin, CreateView):
    form_class = RuangForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('akademik:rb')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Ruang belajar'
        return ctx


class TambahRB(OperasiMixin, CreateView):
    form_class = RBForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('akademik:rb')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Rombongan belajar'
        return ctx


@butuh_operasi
def anggota_rb(request, pk):
    rb = get_object_or_404(RombonganBelajar, pk=pk)
    from kesiswaan.models import Santri
    if request.method == 'POST':
        santri_id = request.POST.get('santri')
        if santri_id:
            KeanggotaanRB.objects.get_or_create(rb=rb, santri_id=santri_id)
            messages.success(request, 'Santri ditambahkan ke RB.')
        return redirect('akademik:rb_detail', pk=pk)
    return render(request, 'pengguna/form_umum.html', {
        'judul': f'Anggota {rb}',
        'form_html': (
            '<div class="mb-3"><label class="form-label">Santri</label>'
            '<select class="form-control" name="santri">'
            + ''.join(
                f'<option value="{s.pk}">{s.nama} ({s.nomor_induk_santri})</option>'
                for s in Santri.objects.filter(status='aktif')
            )
            + '</select></div>'
        ),
        'submit_label': 'Tambah anggota',
    })


@butuh_operasi
def pengampu_rb(request, pk):
    rb = get_object_or_404(RombonganBelajar, pk=pk)
    if request.method == 'POST':
        pegawai_id = request.POST.get('pegawai')
        if pegawai_id:
            PengampuRB.objects.get_or_create(rb=rb, pegawai_id=pegawai_id)
            messages.success(request, 'Pengampu ditugaskan.')
        return redirect('akademik:rb_detail', pk=pk)
    return render(request, 'pengguna/form_umum.html', {
        'judul': f'Pengampu {rb}',
        'form_html': (
            '<div class="mb-3"><label class="form-label">Pegawai</label>'
            '<select class="form-control" name="pegawai">'
            + ''.join(f'<option value="{p.pk}">{p.nama}</option>' for p in Pegawai.objects.filter(aktif=True))
            + '</select></div>'
        ),
        'submit_label': 'Tugaskan',
    })


class DaftarMapel(DaftarFilterMixin, OperasiMixin, ListView):
    model = KitabAtauMapel
    template_name = 'akademik/mapel_list.html'
    context_object_name = 'daftar'
    search_fields = ('nama', 'unit__nama')
    exact_filters = {'jenis': 'jenis', 'unit': 'unit_id'}
    cari_placeholder = 'Nama kitab / mapel'
    export_filename = 'mapel.xlsx'
    export_columns = [
        ('Nama', 'nama'),
        ('Unit', 'unit.nama'),
        ('Jenis', 'get_jenis_display'),
        ('KKM', 'kkm'),
    ]

    def get_filter_fields(self):
        from lembaga.models import UnitPendidikan
        return [
            {'name': 'jenis', 'label': 'Jenis', 'choices': KitabAtauMapel.JENIS},
            {
                'name': 'unit',
                'label': 'Unit',
                'choices': [(u.pk, u.nama) for u in UnitPendidikan.objects.all()],
                'advanced': True,
            },
        ]

    def get_queryset(self):
        return super().get_queryset().select_related('unit', 'jenjang').order_by('nama')


class TambahMapel(OperasiMixin, CreateView):
    form_class = MapelForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('akademik:mapel')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Kitab / mata pelajaran'
        return ctx


@butuh_operasi
def pasang_mapel(request, pk):
    rb = get_object_or_404(RombonganBelajar, pk=pk)
    if request.method == 'POST':
        mapel_id = request.POST.get('mapel')
        if mapel_id:
            MapelRB.objects.get_or_create(rb=rb, mapel_id=mapel_id)
            messages.success(request, 'Mapel dipasang ke RB.')
        return redirect('akademik:rb_detail', pk=pk)
    return render(request, 'pengguna/form_umum.html', {
        'judul': f'Pasang mapel ke {rb}',
        'form_html': (
            '<div class="mb-3"><label class="form-label">Kitab / mapel</label>'
            '<select class="form-control" name="mapel">'
            + ''.join(f'<option value="{m.pk}">{m.nama} ({m.unit})</option>' for m in KitabAtauMapel.objects.all())
            + '</select></div>'
        ),
        'submit_label': 'Pasang',
    })


class DaftarJadwal(DaftarFilterMixin, OperasiMixin, ListView):
    model = JadwalSlot
    template_name = 'akademik/jadwal.html'
    context_object_name = 'daftar'
    search_fields = ('rb__nama', 'mapel__nama', 'pengampu__nama', 'rb__ruang__nama')
    exact_filters = {'hari': 'hari', 'rb': 'rb_id'}
    cari_placeholder = 'RB, mapel, pengampu'
    export_filename = 'jadwal.xlsx'
    export_columns = [
        ('Hari', 'get_hari_display'),
        ('Mulai', 'jam_mulai'),
        ('Selesai', 'jam_selesai'),
        ('RB', 'rb'),
        ('Mapel', 'mapel.nama'),
        ('Pengampu', 'pengampu.nama'),
    ]

    def get_filter_fields(self):
        return [
            {'name': 'hari', 'label': 'Hari', 'choices': JadwalSlot.HARI},
            {
                'name': 'rb',
                'label': 'RB',
                'choices': [(r.pk, str(r)) for r in RombonganBelajar.objects.select_related('ruang', 'tahun_ajaran')],
                'advanced': True,
            },
        ]

    def get_queryset(self):
        qs = JadwalSlot.objects.select_related('rb', 'mapel', 'pengampu').order_by('hari', 'jam_mulai')
        if user_punya_grup(self.request.user, [GRUP_USTADZ]) and not user_punya_grup(
            self.request.user, [GRUP_TU, 'mudir']
        ):
            pegawai = _pegawai(self.request.user)
            if pegawai:
                qs = qs.filter(pengampu=pegawai)
            else:
                qs = qs.none()
        return self.apply_filters(qs)


class TambahJadwal(OperasiMixin, CreateView):
    form_class = JadwalForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('akademik:jadwal')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Slot jadwal'
        return ctx


class DaftarPertemuan(DaftarFilterMixin, OperasiMixin, ListView):
    model = Pertemuan
    template_name = 'akademik/pertemuan_list.html'
    context_object_name = 'daftar'
    search_fields = ('rb__nama', 'mapel__nama', 'pengampu__nama')
    exact_filters = {'rb': 'rb_id', 'mapel': 'mapel_id'}
    date_field = 'tanggal'
    cari_placeholder = 'RB, mapel, pengampu'
    export_filename = 'pertemuan.xlsx'
    export_columns = [
        ('Tanggal', 'tanggal'),
        ('RB', 'rb'),
        ('Mapel', 'mapel.nama'),
        ('Pengampu', 'pengampu.nama'),
        ('Catatan', 'catatan'),
    ]

    def get_filter_fields(self):
        return [
            {
                'name': 'rb',
                'label': 'RB',
                'choices': [(r.pk, str(r)) for r in RombonganBelajar.objects.select_related('ruang', 'tahun_ajaran')],
            },
            {
                'name': 'mapel',
                'label': 'Mapel',
                'choices': [(m.pk, m.nama) for m in KitabAtauMapel.objects.all()],
                'advanced': True,
            },
        ]

    def get_queryset(self):
        qs = Pertemuan.objects.select_related('rb', 'mapel', 'pengampu').order_by('-tanggal')
        pegawai = _pegawai(self.request.user)
        if pegawai and user_punya_grup(self.request.user, [GRUP_USTADZ]) and not user_punya_grup(
            self.request.user, [GRUP_TU, 'mudir']
        ):
            qs = qs.filter(pengampu=pegawai)
        return self.apply_filters(qs)


class TambahPertemuan(OperasiMixin, CreateView):
    form_class = PertemuanForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('akademik:absensi')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Pertemuan'
        return ctx


@butuh_operasi
def isi_absensi(request, pk):
    pertemuan = get_object_or_404(Pertemuan, pk=pk)
    pegawai = _pegawai(request.user)
    if (
        pegawai
        and user_punya_grup(request.user, [GRUP_USTADZ])
        and not user_punya_grup(request.user, [GRUP_TU, 'mudir'])
        and pertemuan.pengampu_id not in (None, pegawai.id)
    ):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Ustadz hanya mengisi RB yang diampu.')
    anggota = list(pertemuan.rb.anggota.select_related('santri'))
    if request.method == 'POST':
        for a in anggota:
            status = request.POST.get(f'status_{a.santri_id}', 'hadir')
            Absensi.objects.update_or_create(
                pertemuan=pertemuan, santri=a.santri, defaults={'status': status},
            )
        messages.success(request, 'Absensi disimpan.')
        return redirect('akademik:absensi')
    tersimpan = {x.santri_id: x.status for x in pertemuan.absensi.all()}
    baris = [
        {'santri': a.santri, 'status': tersimpan.get(a.santri_id, 'hadir')}
        for a in anggota
    ]
    return render(request, 'akademik/absensi.html', {
        'pertemuan': pertemuan,
        'baris': baris,
        'pilihan': Absensi.STATUS,
    })


class DaftarNilai(DaftarFilterMixin, OperasiMixin, ListView):
    model = Penilaian
    template_name = 'akademik/nilai_list.html'
    context_object_name = 'daftar'
    search_fields = ('santri__nama', 'santri__nomor_induk_santri', 'mapel__nama')
    exact_filters = {'periode': 'periode_id', 'mapel': 'mapel_id', 'jenis': 'jenis'}
    cari_placeholder = 'Santri, NIS, mapel'
    export_filename = 'nilai.xlsx'
    export_columns = [
        ('Santri', 'santri.nama'),
        ('Mapel', 'mapel.nama'),
        ('Nilai', 'nilai'),
        ('Predikat', 'predikat'),
        ('Jenis', 'get_jenis_display'),
        ('Periode', 'periode'),
        ('RB', 'rb'),
    ]

    def get_filter_fields(self):
        from lembaga.models import Periode
        return [
            {
                'name': 'periode',
                'label': 'Periode',
                'choices': [(p.pk, str(p)) for p in Periode.objects.select_related('tahun_ajaran')],
            },
            {'name': 'jenis', 'label': 'Jenis', 'choices': Penilaian.JENIS, 'advanced': True},
            {
                'name': 'mapel',
                'label': 'Mapel',
                'choices': [(m.pk, m.nama) for m in KitabAtauMapel.objects.all()],
                'advanced': True,
            },
        ]

    def get_queryset(self):
        return super().get_queryset().select_related('santri', 'mapel', 'periode', 'rb').order_by('-id')


class RekapAbsensi(DaftarFilterMixin, OperasiMixin, ListView):
    model = Santri
    template_name = 'akademik/rekap_absensi.html'
    context_object_name = 'daftar'
    search_fields = ('nama', 'nomor_induk_santri')
    exact_filters = {'status': 'status', 'rb': 'keanggotaan_rb__rb_id'}
    cari_placeholder = 'Nama atau NIS'
    export_filename = 'rekap_absensi.xlsx'
    export_columns = [
        ('NIS', 'nomor_induk_santri'),
        ('Nama', 'nama'),
        ('Hadir', 'n_hadir'),
        ('Izin', 'n_izin'),
        ('Sakit', 'n_sakit'),
        ('Alpa', 'n_alpa'),
        ('Terlambat', 'n_terlambat'),
        ('Alpa beruntun', 'beruntun'),
    ]
    filter_fields = [
        {'name': 'status', 'label': 'Status santri', 'choices': Santri.STATUS},
    ]

    def get_filter_fields(self):
        fields = list(self.filter_fields)
        fields.append({
            'name': 'rb',
            'label': 'RB',
            'choices': [(r.pk, str(r)) for r in RombonganBelajar.objects.select_related('ruang', 'tahun_ajaran')],
            'advanced': True,
        })
        fields.append({
            'name': 'peringatan',
            'label': 'Peringatan alpa',
            'choices': [('1', 'Hanya alpa beruntun')],
            'advanced': True,
        })
        return fields

    def get_queryset(self):
        qs = queryset_rekap_absensi().order_by('nama')
        qs = self.apply_filters(qs).distinct()
        if self.request.GET.get('peringatan') == '1':
            ambang = Pengaturan.get().ambang_alpa
            ids = [s.pk for s in qs if streak_alpa(s) >= ambang]
            qs = qs.filter(pk__in=ids)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ambang = Pengaturan.get().ambang_alpa
        ctx['ambang_alpa'] = ambang
        page = ctx.get('object_list') or []
        ctx['rekap'] = []
        for s in page:
            beruntun = streak_alpa(s)
            ctx['rekap'].append({
                'santri': s,
                'beruntun': beruntun,
                'peringatan': beruntun >= ambang,
            })
        return ctx

    def baris_ekspor(self, obj):
        return [
            obj.nomor_induk_santri,
            obj.nama,
            getattr(obj, 'n_hadir', 0),
            getattr(obj, 'n_izin', 0),
            getattr(obj, 'n_sakit', 0),
            getattr(obj, 'n_alpa', 0),
            getattr(obj, 'n_terlambat', 0),
            streak_alpa(obj),
        ]


@butuh_operasi
def salin_rb_view(request, pk):
    rb = get_object_or_404(RombonganBelajar, pk=pk)
    if request.method != 'POST':
        return redirect('akademik:rb_detail', pk=pk)
    tahun = get_object_or_404(TahunAjaran, pk=request.POST.get('tahun_ajaran') or 0)
    anggota = bool(request.POST.get('salin_anggota'))
    baru = salin_rb(rb, tahun, salin_anggota=anggota)
    messages.success(request, f'RB disalin ke {tahun} sebagai {baru}.')
    return redirect('akademik:rb_detail', pk=baru.pk)


class TambahNilai(OperasiMixin, CreateView):
    form_class = NilaiForm
    template_name = 'pengguna/form_umum.html'
    success_url = reverse_lazy('akademik:nilai')

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = 'Input nilai'
        return ctx
