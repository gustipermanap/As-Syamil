from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.utils import timezone

from akademik.models import KeanggotaanRB, KitabAtauMapel, RombonganBelajar, RuangBelajar
from kesiswaan.models import Pegawai, Santri, WaliSantri
from lembaga.models import Jenjang, Pengaturan, Periode, TahunAjaran, UnitPendidikan
from pengguna.services import pastikan_grup


def buat_user(username, grup, password='sandi123', **kwargs):
    pastikan_grup()
    user, created = User.objects.get_or_create(username=username, defaults=kwargs)
    if created or not user.has_usable_password():
        user.set_password(password)
        user.save()
    g, _ = Group.objects.get_or_create(name=grup)
    user.groups.add(g)
    return user


def data_dasar():
    """Struktur minimal untuk tes lintas modul."""
    pastikan_grup()
    p = Pengaturan.get()
    p.pengelola_keuangan = Pengaturan.PENGELOLA_BENDAHARA
    p.portal_santri_aktif = True
    p.save()
    unit, _ = UnitPendidikan.objects.get_or_create(nama='Diniyah Uji', defaults={'tipe': 'diniyah'})
    tahfidz, _ = UnitPendidikan.objects.get_or_create(nama='Tahfidz Uji', defaults={'tipe': 'tahfidz'})
    asrama, _ = UnitPendidikan.objects.get_or_create(nama='Asrama Uji', defaults={'tipe': 'asrama'})
    jenjang, _ = Jenjang.objects.get_or_create(unit=unit, nama="I'dadiyah", defaults={'urutan': 1})
    hari = date.today()
    ta, _ = TahunAjaran.objects.get_or_create(
        nama='2026/2027-uji',
        defaults={'mulai': hari, 'selesai': hari + timedelta(days=200), 'aktif': True},
    )
    periode, _ = Periode.objects.get_or_create(
        tahun_ajaran=ta, nama='Ganjil uji',
        defaults={'mulai': hari, 'selesai': hari + timedelta(days=100), 'aktif': True},
    )
    ruang, _ = RuangBelajar.objects.get_or_create(
        nama='Halaqah Uji', defaults={'unit': unit, 'jenjang': jenjang, 'tipe': 'halaqah'},
    )
    rb, _ = RombonganBelajar.objects.get_or_create(
        ruang=ruang, tahun_ajaran=ta, defaults={'nama': 'RB Uji'},
    )
    return {
        'pengaturan': p,
        'unit': unit,
        'tahfidz': tahfidz,
        'asrama': asrama,
        'jenjang': jenjang,
        'ta': ta,
        'periode': periode,
        'ruang': ruang,
        'rb': rb,
    }


def buat_santri(nis, nama, nik, jk='L', wali=None, status='aktif'):
    return Santri.objects.create(
        nomor_induk_santri=nis,
        nama=nama,
        nik=nik,
        jenis_kelamin=jk,
        status=status,
        wali=wali,
        tanggal_lahir=date(2012, 1, 1),
        nisn='1234567890',
    )
