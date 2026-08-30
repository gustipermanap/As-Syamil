from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class RuangBelajar(models.Model):
    TIPE = [
        ('kelas', 'Kelas'),
        ('halaqah', 'Halaqah'),
        ('kelompok_tahfidz', 'Kelompok tahfidz'),
    ]
    unit = models.ForeignKey('lembaga.UnitPendidikan', on_delete=models.CASCADE, related_name='ruang')
    jenjang = models.ForeignKey('lembaga.Jenjang', on_delete=models.SET_NULL, null=True, blank=True)
    nama = models.CharField(max_length=80)
    tipe = models.CharField(max_length=30, choices=TIPE, default='halaqah')

    class Meta:
        verbose_name = 'Ruang belajar'
        verbose_name_plural = 'Ruang belajar'

    def __str__(self):
        return self.nama


class RombonganBelajar(models.Model):
    ruang = models.ForeignKey(RuangBelajar, on_delete=models.CASCADE, related_name='rombongan')
    tahun_ajaran = models.ForeignKey('lembaga.TahunAjaran', on_delete=models.CASCADE, related_name='rombongan')
    nama = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = 'Rombongan belajar'
        verbose_name_plural = 'Rombongan belajar'
        unique_together = ('ruang', 'tahun_ajaran')

    def __str__(self):
        return self.nama or f'{self.ruang} ({self.tahun_ajaran})'


class PengampuRB(models.Model):
    rb = models.ForeignKey(RombonganBelajar, on_delete=models.CASCADE, related_name='pengampu')
    pegawai = models.ForeignKey('kesiswaan.Pegawai', on_delete=models.CASCADE, related_name='ampuan')
    sebagai_wali = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pengampu RB'
        verbose_name_plural = 'Pengampu RB'
        unique_together = ('rb', 'pegawai')


class KeanggotaanRB(models.Model):
    rb = models.ForeignKey(RombonganBelajar, on_delete=models.CASCADE, related_name='anggota')
    santri = models.ForeignKey('kesiswaan.Santri', on_delete=models.CASCADE, related_name='keanggotaan_rb')

    class Meta:
        verbose_name = 'Keanggotaan RB'
        verbose_name_plural = 'Keanggotaan RB'
        unique_together = ('rb', 'santri')


class KitabAtauMapel(models.Model):
    JENIS = [
        ('kitab', 'Kitab'),
        ('mapel_umum', 'Mapel umum'),
        ('mapel_diniyah', 'Mapel diniyah'),
    ]
    unit = models.ForeignKey('lembaga.UnitPendidikan', on_delete=models.CASCADE, related_name='mapel')
    jenjang = models.ForeignKey('lembaga.Jenjang', on_delete=models.SET_NULL, null=True, blank=True)
    nama = models.CharField(max_length=120)
    jenis = models.CharField(max_length=20, choices=JENIS, default='kitab')
    kkm = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Kitab / mata pelajaran'
        verbose_name_plural = 'Kitab / mata pelajaran'

    def __str__(self):
        return self.nama


class MapelRB(models.Model):
    rb = models.ForeignKey(RombonganBelajar, on_delete=models.CASCADE, related_name='mapel_rb')
    mapel = models.ForeignKey(KitabAtauMapel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rb', 'mapel')


class JadwalSlot(models.Model):
    HARI = [
        (0, 'Senin'), (1, 'Selasa'), (2, 'Rabu'), (3, 'Kamis'),
        (4, 'Jumat'), (5, 'Sabtu'), (6, 'Ahad'),
    ]
    rb = models.ForeignKey(RombonganBelajar, on_delete=models.CASCADE, related_name='jadwal')
    hari = models.PositiveSmallIntegerField(choices=HARI)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    mapel = models.ForeignKey(KitabAtauMapel, on_delete=models.CASCADE)
    pengampu = models.ForeignKey('kesiswaan.Pegawai', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Jadwal'
        verbose_name_plural = 'Jadwal'


class Pertemuan(models.Model):
    slot = models.ForeignKey(JadwalSlot, on_delete=models.SET_NULL, null=True, blank=True)
    rb = models.ForeignKey(RombonganBelajar, on_delete=models.CASCADE, related_name='pertemuan')
    mapel = models.ForeignKey(KitabAtauMapel, on_delete=models.CASCADE)
    pengampu = models.ForeignKey('kesiswaan.Pegawai', on_delete=models.SET_NULL, null=True, blank=True)
    tanggal = models.DateField()
    catatan = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Pertemuan'
        verbose_name_plural = 'Pertemuan'


class Absensi(models.Model):
    STATUS = [
        ('hadir', 'Hadir'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
        ('alpa', 'Alpa'),
        ('terlambat', 'Terlambat'),
    ]
    pertemuan = models.ForeignKey(Pertemuan, on_delete=models.CASCADE, related_name='absensi')
    santri = models.ForeignKey('kesiswaan.Santri', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='hadir')

    class Meta:
        verbose_name = 'Absensi'
        verbose_name_plural = 'Absensi'
        unique_together = ('pertemuan', 'santri')


class Penilaian(models.Model):
    JENIS = [
        ('harian', 'Harian'),
        ('ujian', 'Ujian'),
        ('akhir', 'Akhir periode'),
    ]
    santri = models.ForeignKey('kesiswaan.Santri', on_delete=models.CASCADE, related_name='nilai')
    mapel = models.ForeignKey(KitabAtauMapel, on_delete=models.CASCADE)
    rb = models.ForeignKey(RombonganBelajar, on_delete=models.CASCADE)
    periode = models.ForeignKey('lembaga.Periode', on_delete=models.CASCADE)
    jenis = models.CharField(max_length=20, choices=JENIS, default='harian')
    nilai = models.DecimalField(max_digits=5, decimal_places=1)
    predikat = models.CharField(max_length=2, blank=True)

    class Meta:
        verbose_name = 'Penilaian'
        verbose_name_plural = 'Penilaian'

    def clean(self):
        if self.nilai is not None and (self.nilai < 0 or self.nilai > 100):
            raise ValidationError({'nilai': 'Nilai harus 0–100.'})

    def save(self, *args, **kwargs):
        from lembaga.models import Pengaturan
        self.predikat = Pengaturan.get().predikat(float(self.nilai))
        self.full_clean()
        super().save(*args, **kwargs)
