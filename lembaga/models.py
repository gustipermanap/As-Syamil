from django.core.exceptions import ValidationError
from django.db import models


class Pengaturan(models.Model):
    PENGELOLA_BENDAHARA = 'bendahara'
    PENGELOLA_TU = 'tata_usaha'
    PENGELOLA_CHOICES = [
        (PENGELOLA_BENDAHARA, 'Bendahara'),
        (PENGELOLA_TU, 'Tata Usaha'),
    ]
    PERIODE_SEMESTER = 'semester'
    PERIODE_CATURWULAN = 'caturwulan'
    PERIODE_CHOICES = [
        (PERIODE_SEMESTER, 'Semester'),
        (PERIODE_CATURWULAN, 'Caturwulan'),
    ]

    nama_tampil = models.CharField(max_length=120, default='Pondok Pesantren As-Syamil')
    nsm = models.CharField(max_length=20, blank=True)
    npsn = models.CharField(max_length=20, blank=True)
    pengelola_keuangan = models.CharField(
        max_length=20,
        choices=PENGELOLA_CHOICES,
        default=PENGELOLA_BENDAHARA,
    )
    portal_santri_aktif = models.BooleanField(default=False)
    jenis_periode = models.CharField(max_length=20, choices=PERIODE_CHOICES, default=PERIODE_SEMESTER)
    modul_ppdb = models.BooleanField(default=True)
    modul_akademik = models.BooleanField(default=True)
    modul_tahfidz = models.BooleanField(default=True)
    modul_asrama = models.BooleanField(default=True)
    modul_keuangan = models.BooleanField(default=True)
    modul_kedisiplinan = models.BooleanField(default=True)
    predikat_a = models.PositiveSmallIntegerField(default=90)
    predikat_b = models.PositiveSmallIntegerField(default=80)
    predikat_c = models.PositiveSmallIntegerField(default=70)
    predikat_d = models.PositiveSmallIntegerField(default=60)
    ambang_alpa = models.PositiveSmallIntegerField(default=3)

    class Meta:
        verbose_name = 'Pengaturan lembaga'
        verbose_name_plural = 'Pengaturan lembaga'

    def __str__(self):
        return self.nama_tampil

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def predikat(self, nilai):
        if nilai is None:
            return ''
        if nilai >= self.predikat_a:
            return 'A'
        if nilai >= self.predikat_b:
            return 'B'
        if nilai >= self.predikat_c:
            return 'C'
        if nilai >= self.predikat_d:
            return 'D'
        return 'E'


class UnitPendidikan(models.Model):
    TIPE_CHOICES = [
        ('formal', 'Formal'),
        ('diniyah', 'Diniyah'),
        ('tahfidz', 'Tahfidz'),
        ('asrama', 'Asrama'),
    ]
    nama = models.CharField(max_length=100)
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)
    aktif = models.BooleanField(default=True)
    label_peserta = models.CharField(max_length=30, default='Santri')

    class Meta:
        verbose_name = 'Unit pendidikan'
        verbose_name_plural = 'Unit pendidikan'

    def __str__(self):
        return self.nama


class Jenjang(models.Model):
    unit = models.ForeignKey(UnitPendidikan, on_delete=models.CASCADE, related_name='jenjang')
    nama = models.CharField(max_length=80)
    urutan = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Jenjang'
        verbose_name_plural = 'Jenjang'
        ordering = ['unit', 'urutan', 'nama']

    def __str__(self):
        return f'{self.unit.nama} — {self.nama}'


class TahunAjaran(models.Model):
    nama = models.CharField(max_length=20, help_text='Contoh: 2026/2027')
    mulai = models.DateField()
    selesai = models.DateField()
    aktif = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tahun ajaran'
        verbose_name_plural = 'Tahun ajaran'
        ordering = ['-mulai']

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.aktif:
            TahunAjaran.objects.exclude(pk=self.pk).update(aktif=False)


class Periode(models.Model):
    tahun_ajaran = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE, related_name='periode')
    nama = models.CharField(max_length=40)
    mulai = models.DateField()
    selesai = models.DateField()
    aktif = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Periode'
        verbose_name_plural = 'Periode'

    def __str__(self):
        return f'{self.tahun_ajaran} {self.nama}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.aktif:
            Periode.objects.filter(tahun_ajaran=self.tahun_ajaran).exclude(pk=self.pk).update(aktif=False)
