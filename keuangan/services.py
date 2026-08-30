import secrets
from django.db import transaction
from django.utils import timezone

from kesiswaan.models import Santri
from .models import JenisTagihan, Pembayaran, Tagihan


def generate_tagihan_massal(jenis, jumlah, jatuh_tempo, periode=None, rb=None):
    sasaran = Santri.objects.filter(status='aktif')
    if rb:
        sasaran = sasaran.filter(keanggotaan_rb__rb=rb)
    dibuat = []
    for santri in sasaran.distinct():
        obj, created = Tagihan.objects.get_or_create(
            santri=santri,
            jenis=jenis,
            periode=periode,
            defaults={'jumlah': jumlah, 'jatuh_tempo': jatuh_tempo},
        )
        if created:
            dibuat.append(obj)
    return dibuat


def nomor_kwitansi():
    return timezone.now().strftime('KW%Y%m%d%H%M%S') + secrets.token_hex(3).upper()


def terima_bayar(tagihan, jumlah, user, metode='tunai'):
    with transaction.atomic():
        bayar = Pembayaran(
            tagihan=tagihan,
            jumlah=jumlah,
            metode=metode,
            nomor_kwitansi=nomor_kwitansi(),
            penerima=user,
        )
        bayar.full_clean()
        bayar.save()
        tagihan.refresh_status()
    return bayar
