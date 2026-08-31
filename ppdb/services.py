import secrets
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.utils import timezone

from kesiswaan.models import PenempatanKamar, Santri, WaliSantri
from akademik.models import KeanggotaanRB
from .models import GelombangPPDB, gelombang_terbuka


def buat_kode():
    return secrets.token_hex(4).upper()


def terima_menjadi_santri(pendaftaran, prefix_nis='ASY', rb=None, kamar=None):
    if pendaftaran.status != 'diterima':
        pendaftaran.status = 'diterima'
        pendaftaran.save(update_fields=['status'])
    if Santri.objects.filter(pendaftaran=pendaftaran).exists():
        santri = Santri.objects.get(pendaftaran=pendaftaran)
    else:
        with transaction.atomic():
            wali, _ = WaliSantri.objects.get_or_create(
                nama=pendaftaran.nama_ayah or 'Wali',
                defaults={'kontak': pendaftaran.no_handphone, 'alamat': pendaftaran.alamat or ''},
            )
            urut = Santri.objects.count() + 1
            nis = f'{prefix_nis}{timezone.now().year}{urut:04d}'
            while Santri.objects.filter(nomor_induk_santri=nis).exists():
                urut += 1
                nis = f'{prefix_nis}{timezone.now().year}{urut:04d}'
            santri = Santri.objects.create(
                nomor_induk_santri=nis,
                nisn=pendaftaran.nisn or '',
                nama=pendaftaran.nama_lengkap,
                nik=pendaftaran.nik,
                tempat_lahir=pendaftaran.tempat_lahir,
                tanggal_lahir=pendaftaran.tanggal_lahir,
                jenis_kelamin=pendaftaran.jenis_kelamin,
                status='aktif',
                wali=wali,
                alamat=pendaftaran.alamat or '',
                pendaftaran=pendaftaran,
            )
            if pendaftaran.foto:
                santri.foto = pendaftaran.foto
                santri.save(update_fields=['foto'])
    if rb:
        KeanggotaanRB.objects.get_or_create(rb=rb, santri=santri)
    if kamar:
        from datetime import date
        if not PenempatanKamar.objects.filter(santri=santri, keluar__isnull=True).exists():
            PenempatanKamar.objects.create(santri=santri, kamar=kamar, masuk=date.today())
    if pendaftaran.gelombang_id:
        gelombang = GelombangPPDB.objects.filter(pk=pendaftaran.gelombang_id).first()
        if gelombang:
            gelombang.tutup_jika_kuota_penuh()
    return santri
