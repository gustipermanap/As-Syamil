from .models import LogAkses, Notifikasi


def kirim_notifikasi(user, judul, isi='', tautan=''):
    if not user:
        return None
    return Notifikasi.objects.create(
        penerima=user, judul=judul, isi=isi, tautan=tautan or '',
    )


def catat_akses(user, aksi, objek='', ringkas=''):
    return LogAkses.objects.create(
        user=user if getattr(user, 'is_authenticated', False) else None,
        aksi=aksi,
        objek=objek,
        ringkas=ringkas,
    )


def tautan_izin(izin):
    from pengguna.models import GRUP_SANTRI
    from pengguna.services import user_punya_grup
    if izin.pemohon_id and user_punya_grup(izin.pemohon, GRUP_SANTRI):
        return '/santri/'
    return '/wali/'
