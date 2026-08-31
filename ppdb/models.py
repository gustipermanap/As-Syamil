from django.db import models
from django.utils import timezone


class GelombangPPDB(models.Model):
    DRAF = 'draf'
    DIBUKA = 'dibuka'
    DITUTUP = 'ditutup'
    SELEKSI = 'seleksi'
    SELESAI = 'selesai'
    STATUS = [
        (DRAF, 'Draf'),
        (DIBUKA, 'Dibuka'),
        (DITUTUP, 'Ditutup'),
        (SELEKSI, 'Seleksi'),
        (SELESAI, 'Selesai'),
    ]
    nama = models.CharField(max_length=80)
    mulai = models.DateTimeField()
    selesai = models.DateTimeField()
    kuota = models.PositiveIntegerField(default=50)
    status = models.CharField(max_length=20, choices=STATUS, default=DRAF)
    biaya_pendaftaran = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    unit_tujuan = models.ForeignKey(
        'lembaga.UnitPendidikan', on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Gelombang PPDB'
        verbose_name_plural = 'Gelombang PPDB'
        ordering = ['-mulai']

    def __str__(self):
        return self.nama

    def efektif_dibuka(self, saat=None):
        saat = saat or timezone.now()
        if self.status != self.DIBUKA:
            return False
        return self.mulai <= saat <= self.selesai

    def tutup_jika_lewat(self, saat=None):
        saat = saat or timezone.now()
        if self.status == self.DIBUKA and saat > self.selesai:
            self.status = self.DITUTUP
            self.save(update_fields=['status'])
        return self.status

    def jumlah_diterima(self):
        return self.pendaftar.filter(status='diterima').count()

    def sisa_kuota(self):
        sisa = self.kuota - self.jumlah_diterima()
        return sisa if sisa > 0 else 0

    def tutup_jika_kuota_penuh(self):
        if self.status == self.DIBUKA and self.kuota and self.jumlah_diterima() >= self.kuota:
            self.status = self.DITUTUP
            self.save(update_fields=['status'])
        return self.status


def gelombang_terbuka():
    sekarang = timezone.now()
    for g in GelombangPPDB.objects.filter(status=GelombangPPDB.DIBUKA):
        g.tutup_jika_lewat(sekarang)
        g.tutup_jika_kuota_penuh()
        if g.efektif_dibuka(sekarang) and g.sisa_kuota() > 0:
            return g
    return None


def gelombang_berikutnya():
    sekarang = timezone.now()
    return (
        GelombangPPDB.objects.filter(mulai__gt=sekarang)
        .exclude(status=GelombangPPDB.SELESAI)
        .order_by('mulai')
        .first()
    )
