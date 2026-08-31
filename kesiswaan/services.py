from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.utils import timezone

from pengguna.models import GRUP_SANTRI, GRUP_WALI
from pengguna.notifikasi import kirim_notifikasi, tautan_izin
from .models import PenempatanKamar, Santri


def anak_wali(user):
    wali = getattr(user, 'wali_santri', None)
    if user.is_superuser and not wali:
        return Santri.objects.all()
    if not wali:
        return Santri.objects.none()
    return Santri.objects.filter(wali=wali)


def santri_portal(user):
    return getattr(user, 'akun_santri', None)


def tautkan_akun_pegawai(pegawai, username, sandi, grup):
    user = pegawai.user
    if user:
        if sandi:
            user.set_password(sandi)
            user.save()
        if grup:
            user.groups.clear()
            g, _ = Group.objects.get_or_create(name=grup)
            user.groups.add(g)
        return pegawai
    if not username or not sandi:
        return pegawai
    if User.objects.filter(username=username).exists():
        raise ValidationError('Nama pengguna sudah dipakai.')
    user = User.objects.create_user(username=username, password=sandi)
    pegawai.user = user
    pegawai.save()
    if grup:
        g, _ = Group.objects.get_or_create(name=grup)
        user.groups.add(g)
    return pegawai


def tautkan_akun_wali(wali, username, sandi):
    if wali.user_id:
        if sandi:
            wali.user.set_password(sandi)
            wali.user.save()
        return wali
    if not username or not sandi:
        return wali
    if User.objects.filter(username=username).exists():
        raise ValidationError('Nama pengguna sudah dipakai.')
    user = User.objects.create_user(username=username, password=sandi)
    g, _ = Group.objects.get_or_create(name=GRUP_WALI)
    user.groups.add(g)
    wali.user = user
    wali.save()
    return wali


def tautkan_akun_santri(santri, username, sandi):
    if santri.user_id:
        if sandi:
            santri.user.set_password(sandi)
            santri.user.save()
        return santri
    if not username or not sandi:
        return santri
    if User.objects.filter(username=username).exists():
        raise ValidationError('Nama pengguna sudah dipakai.')
    user = User.objects.create_user(username=username, password=sandi)
    g, _ = Group.objects.get_or_create(name=GRUP_SANTRI)
    user.groups.add(g)
    santri.user = user
    santri.save()
    return santri


def proses_izin(izin, aksi, saat=None):
    saat = saat or timezone.now()
    if aksi == 'setujui':
        if izin.status != 'diajukan':
            raise ValidationError('Hanya izin diajukan yang dapat disetujui.')
        izin.status = 'disetujui'
    elif aksi == 'tolak':
        if izin.status != 'diajukan':
            raise ValidationError('Hanya izin diajukan yang dapat ditolak.')
        izin.status = 'ditolak'
    elif aksi == 'mulai':
        if izin.status != 'disetujui':
            raise ValidationError('Izin harus disetujui sebelum berlangsung.')
        izin.status = 'berlangsung'
    elif aksi == 'kembali':
        if izin.status not in ('disetujui', 'berlangsung'):
            raise ValidationError('Izin ini belum bisa ditandai kembali.')
        izin.status = 'terlambat' if saat > izin.selesai else 'selesai'
    else:
        raise ValidationError('Aksi izin tidak dikenal.')
    izin.save(update_fields=['status'])
    if aksi in ('setujui', 'tolak') and izin.pemohon_id:
        kirim_notifikasi(
            izin.pemohon,
            f'Izin {izin.get_status_display()}',
            f'Izin {izin.santri.nama} sekarang {izin.get_status_display()}.',
            tautan=tautan_izin(izin),
        )
    return izin


def pindah_kamar(santri, kamar_baru, tanggal):
    aktif = list(PenempatanKamar.objects.filter(santri=santri, keluar__isnull=True))
    for penempatan in aktif:
        penempatan.keluar = tanggal
        penempatan.save()
    return PenempatanKamar.objects.create(santri=santri, kamar=kamar_baru, masuk=tanggal)
