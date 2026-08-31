from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class JenisTagihan(models.Model):
    nama = models.CharField(max_length=80)
    deskripsi = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Jenis tagihan'
        verbose_name_plural = 'Jenis tagihan'

    def __str__(self):
        return self.nama


class Tagihan(models.Model):
    BELUM = 'belum'
    SEBAGIAN = 'sebagian'
    LUNAS = 'lunas'
    BATAL = 'batal'
    STATUS = [
        (BELUM, 'Belum'),
        (SEBAGIAN, 'Sebagian'),
        (LUNAS, 'Lunas'),
        (BATAL, 'Batal'),
    ]
    santri = models.ForeignKey('kesiswaan.Santri', on_delete=models.CASCADE, related_name='tagihan')
    jenis = models.ForeignKey(JenisTagihan, on_delete=models.PROTECT)
    periode = models.ForeignKey('lembaga.Periode', on_delete=models.CASCADE, null=True, blank=True)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    potongan = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    jatuh_tempo = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default=BELUM)

    class Meta:
        verbose_name = 'Tagihan'
        verbose_name_plural = 'Tagihan'
        unique_together = ('santri', 'jenis', 'periode')

    def __str__(self):
        return f'{self.santri} {self.jenis}'

    def terbayar(self):
        from django.db.models import Sum
        return self.pembayaran.aggregate(s=Sum('jumlah'))['s'] or 0

    def jumlah_netto(self):
        from decimal import Decimal
        potongan = self.potongan or Decimal('0')
        nilai = self.jumlah - potongan
        return nilai if nilai > 0 else Decimal('0')

    def sisa(self):
        return self.jumlah_netto() - self.terbayar()

    def clean(self):
        from decimal import Decimal
        potongan = self.potongan or Decimal('0')
        if potongan < 0:
            raise ValidationError({'potongan': 'Potongan tidak boleh negatif.'})
        if potongan > self.jumlah:
            raise ValidationError({'potongan': 'Potongan tidak boleh melebihi jumlah tagihan.'})

    def refresh_status(self):
        if self.status == self.BATAL:
            return
        terbayar = self.terbayar()
        netto = self.jumlah_netto()
        if netto <= 0:
            self.status = self.LUNAS
        elif terbayar <= 0:
            self.status = self.BELUM
        elif terbayar >= netto:
            self.status = self.LUNAS
        else:
            self.status = self.SEBAGIAN
        self.save(update_fields=['status'])


class Pembayaran(models.Model):
    METODE = [
        ('tunai', 'Tunai'),
        ('transfer', 'Transfer'),
        ('lainnya', 'Lainnya'),
    ]
    tagihan = models.ForeignKey(Tagihan, on_delete=models.CASCADE, related_name='pembayaran')
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal = models.DateField(default=timezone.now)
    metode = models.CharField(max_length=20, choices=METODE, default='tunai')
    nomor_kwitansi = models.CharField(max_length=30, unique=True)
    penerima = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Pembayaran'
        verbose_name_plural = 'Pembayaran'

    def clean(self):
        sisa = self.tagihan.sisa()
        if self.pk:
            lama = Pembayaran.objects.get(pk=self.pk)
            sisa += lama.jumlah
        if self.jumlah > sisa:
            raise ValidationError({'jumlah': 'Pembayaran melebihi sisa tagihan.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.tagihan.refresh_status()
