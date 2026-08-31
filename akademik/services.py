from django.db.models import Count, Q

from lembaga.models import Pengaturan
from .models import Absensi, JadwalSlot, KeanggotaanRB, MapelRB, PengampuRB, RombonganBelajar


def salin_rb(rb_sumber, tahun_tujuan, salin_anggota=False):
    rb_baru, _ = RombonganBelajar.objects.get_or_create(
        ruang=rb_sumber.ruang,
        tahun_ajaran=tahun_tujuan,
        defaults={'nama': rb_sumber.nama},
    )
    if not rb_baru.nama and rb_sumber.nama:
        rb_baru.nama = rb_sumber.nama
        rb_baru.save(update_fields=['nama'])
    for p in rb_sumber.pengampu.all():
        PengampuRB.objects.get_or_create(
            rb=rb_baru, pegawai=p.pegawai, defaults={'sebagai_wali': p.sebagai_wali},
        )
    for m in rb_sumber.mapel_rb.all():
        MapelRB.objects.get_or_create(rb=rb_baru, mapel=m.mapel)
    for j in rb_sumber.jadwal.all():
        JadwalSlot.objects.get_or_create(
            rb=rb_baru, hari=j.hari, jam_mulai=j.jam_mulai, jam_selesai=j.jam_selesai,
            mapel=j.mapel, defaults={'pengampu': j.pengampu},
        )
    if salin_anggota:
        for a in rb_sumber.anggota.all():
            KeanggotaanRB.objects.get_or_create(rb=rb_baru, santri=a.santri)
    return rb_baru


def streak_alpa(santri):
    baris = (
        Absensi.objects.filter(santri=santri)
        .select_related('pertemuan')
        .order_by('-pertemuan__tanggal', '-id')
    )
    n = 0
    for r in baris:
        if r.status == 'alpa':
            n += 1
        else:
            break
    return n


def queryset_rekap_absensi():
    from kesiswaan.models import Santri
    return Santri.objects.annotate(
        n_hadir=Count('absensi', filter=Q(absensi__status='hadir')),
        n_izin=Count('absensi', filter=Q(absensi__status='izin')),
        n_sakit=Count('absensi', filter=Q(absensi__status='sakit')),
        n_alpa=Count('absensi', filter=Q(absensi__status='alpa')),
        n_terlambat=Count('absensi', filter=Q(absensi__status='terlambat')),
    )


def tandai_peringatan_alpa(santri_list):
    ambang = Pengaturan.get().ambang_alpa
    hasil = []
    for s in santri_list:
        beruntun = streak_alpa(s)
        hasil.append({
            'santri': s,
            'beruntun': beruntun,
            'peringatan': beruntun >= ambang,
            'ambang': ambang,
        })
    return hasil
