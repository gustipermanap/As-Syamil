from django.db import models


class ProgressHafalan(models.Model):
    santri = models.OneToOneField('kesiswaan.Santri', on_delete=models.CASCADE, related_name='progress_hafalan')
    juz_selesai = models.PositiveSmallIntegerField(default=0)
    halaman_berjalan = models.PositiveSmallIntegerField(default=1)
    target_juz = models.PositiveSmallIntegerField(default=30)

    class Meta:
        verbose_name = 'Progress hafalan'
        verbose_name_plural = 'Progress hafalan'

    def __str__(self):
        return f'{self.santri} juz {self.juz_selesai}'


class SetoranHafalan(models.Model):
    ZIYADAH = 'ziyadah'
    MUROJAAH = 'murojaah'
    TASMI = 'tasmi'
    JENIS = [
        (ZIYADAH, 'Ziyadah'),
        (MUROJAAH, 'Muroja’ah'),
        (TASMI, 'Tasmi’'),
    ]
    MUTU = [
        ('lancar', 'Lancar'),
        ('cukup', 'Cukup'),
        ('kurang', 'Kurang'),
    ]
    santri = models.ForeignKey('kesiswaan.Santri', on_delete=models.CASCADE, related_name='setoran')
    jenis = models.CharField(max_length=20, choices=JENIS)
    dari_juz = models.PositiveSmallIntegerField()
    dari_halaman = models.PositiveSmallIntegerField()
    sampai_juz = models.PositiveSmallIntegerField()
    sampai_halaman = models.PositiveSmallIntegerField()
    mutu = models.CharField(max_length=10, choices=MUTU)
    catatan_tajwid = models.TextField(blank=True)
    penyimak = models.ForeignKey('kesiswaan.Pegawai', on_delete=models.SET_NULL, null=True, blank=True)
    tanggal = models.DateField()

    class Meta:
        verbose_name = 'Setoran hafalan'
        verbose_name_plural = 'Setoran hafalan'
        ordering = ['-tanggal']

    def __str__(self):
        return f'{self.santri} {self.jenis} {self.tanggal}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from tahfidz.services import catat_setoran
        catat_setoran(self)
