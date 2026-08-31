from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Izin, PenempatanKamar, Santri


def anak_wali(user):
    wali = getattr(user, 'wali_santri', None)
    if user.is_superuser and not wali:
        return Santri.objects.all()
    if not wali:
        return Santri.objects.none()
    return Santri.objects.filter(wali=wali)


def santri_portal(user):
    return getattr(user, 'akun_santri', None)


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
    return izin


def pindah_kamar(santri, kamar_baru, tanggal):
    aktif = list(PenempatanKamar.objects.filter(santri=santri, keluar__isnull=True))
    for penempatan in aktif:
        penempatan.keluar = tanggal
        penempatan.save()
    return PenempatanKamar.objects.create(santri=santri, kamar=kamar_baru, masuk=tanggal)


def anak_wali(user):
    wali = getattr(user, 'wali_santri', None)
    if user.is_superuser and not wali:
        return Santri.objects.all()
    if not wali:
        return Santri.objects.none()
    return Santri.objects.filter(wali=wali)


def santri_portal(user):
    return getattr(user, 'akun_santri', None)


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
    return izin
