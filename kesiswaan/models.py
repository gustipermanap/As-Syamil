from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Pegawai(models.Model):
    JENIS_KELAMIN = [('L', 'Laki-laki'), ('P', 'Perempuan')]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='pegawai',
    )
    nama = models.CharField(max_length=120)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    kontak = models.CharField(max_length=30, blank=True)
    aktif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pegawai'
        verbose_name_plural = 'Pegawai'

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user_id:
            if self.user.is_active != self.aktif:
                self.user.is_active = self.aktif
                self.user.save(update_fields=['is_active'])


class WaliSantri(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='wali_santri',
    )
    nama = models.CharField(max_length=120)
    hubungan = models.CharField(max_length=40, default='Orang tua')
    kontak = models.CharField(max_length=30, blank=True)
    alamat = models.TextField(blank=True)
    pekerjaan = models.CharField(max_length=80, blank=True)
    penghasilan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Wali santri'
        verbose_name_plural = 'Wali santri'

    def __str__(self):
        return self.nama


class Santri(models.Model):
    JENIS_KELAMIN = [('L', 'Laki-laki'), ('P', 'Perempuan')]
    STATUS = [
        ('calon', 'Calon'),
        ('aktif', 'Aktif'),
        ('izin_panjang', 'Izin panjang'),
        ('lulus', 'Lulus'),
        ('keluar', 'Keluar'),
        ('dikeluarkan', 'Dikeluarkan'),
    ]
    nomor_induk_santri = models.CharField(max_length=20, unique=True)
    nisn = models.CharField(max_length=12, blank=True)
    nama = models.CharField(max_length=120)
    nik = models.CharField(max_length=16)
    tempat_lahir = models.CharField(max_length=80, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    status = models.CharField(max_length=20, choices=STATUS, default='aktif')
    wali = models.ForeignKey(WaliSantri, on_delete=models.SET_NULL, null=True, blank=True, related_name='santri')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='akun_santri',
    )
    foto = models.ImageField(upload_to='santri/', blank=True, null=True)
    alamat = models.TextField(blank=True)
    pendaftaran = models.ForeignKey(
        'WebApp.Pendaftaran', on_delete=models.SET_NULL, null=True, blank=True, related_name='santri_hasil',
    )

    class Meta:
        verbose_name = 'Santri'
        verbose_name_plural = 'Santri'

    def __str__(self):
        return f'{self.nomor_induk_santri} — {self.nama}'

    def clean(self):
        if self.nik and not (len(self.nik) == 16 and self.nik.isdigit()):
            raise ValidationError({'nik': 'NIK harus 16 digit.'})
        if self.nisn and not (10 <= len(self.nisn) <= 12 and self.nisn.isdigit()):
            raise ValidationError({'nisn': 'NISN harus 10–12 digit.'})
        if self.nik and self.status == 'aktif':
            bentrok = Santri.objects.filter(nik=self.nik, status='aktif').exclude(pk=self.pk)
            if bentrok.exists():
                raise ValidationError({'nik': 'NIK sudah dipakai santri aktif lain.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Gedung(models.Model):
    nama = models.CharField(max_length=80)
    putra_putri = models.CharField(max_length=1, choices=[('L', 'Putra'), ('P', 'Putri')])

    class Meta:
        verbose_name = 'Gedung'
        verbose_name_plural = 'Gedung'

    def __str__(self):
        return self.nama


class Kamar(models.Model):
    gedung = models.ForeignKey(Gedung, on_delete=models.CASCADE, related_name='kamar')
    nama = models.CharField(max_length=40)
    kapasitas = models.PositiveSmallIntegerField(default=8)

    class Meta:
        verbose_name = 'Kamar'
        verbose_name_plural = 'Kamar'

    def __str__(self):
        return f'{self.gedung} / {self.nama}'

    def terisi(self):
        return self.penempatan.filter(keluar__isnull=True).count()


class PenempatanKamar(models.Model):
    santri = models.ForeignKey(Santri, on_delete=models.CASCADE, related_name='penempatan_kamar')
    kamar = models.ForeignKey(Kamar, on_delete=models.CASCADE, related_name='penempatan')
    masuk = models.DateField()
    keluar = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Penempatan kamar'
        verbose_name_plural = 'Penempatan kamar'

    def clean(self):
        if self.kamar.gedung.putra_putri != self.santri.jenis_kelamin:
            raise ValidationError('Jenis kelamin santri tidak sesuai kamar.')
        aktif_lain = PenempatanKamar.objects.filter(santri=self.santri, keluar__isnull=True).exclude(pk=self.pk)
        if self.keluar is None and aktif_lain.exists():
            raise ValidationError('Santri sudah punya kamar aktif.')
        if self.keluar is None and self.kamar.terisi() >= self.kamar.kapasitas:
            if not PenempatanKamar.objects.filter(pk=self.pk, kamar=self.kamar, keluar__isnull=True).exists():
                raise ValidationError('Kamar penuh.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Izin(models.Model):
    JENIS = [
        ('pulang', 'Pulang'),
        ('sakit', 'Sakit'),
        ('keperluan', 'Keperluan'),
        ('terlambat_kembali', 'Terlambat kembali'),
    ]
    STATUS = [
        ('diajukan', 'Diajukan'),
        ('disetujui', 'Disetujui'),
        ('ditolak', 'Ditolak'),
        ('berlangsung', 'Berlangsung'),
        ('selesai', 'Selesai'),
        ('terlambat', 'Terlambat'),
    ]
    santri = models.ForeignKey(Santri, on_delete=models.CASCADE, related_name='izin')
    jenis = models.CharField(max_length=30, choices=JENIS)
    status = models.CharField(max_length=20, choices=STATUS, default='diajukan')
    mulai = models.DateTimeField()
    selesai = models.DateTimeField()
    alasan = models.TextField(blank=True)
    pemohon = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Izin'
        verbose_name_plural = 'Izin'

    def __str__(self):
        return f'{self.santri} {self.jenis}'


class JenisPelanggaran(models.Model):
    nama = models.CharField(max_length=80)
    poin = models.PositiveSmallIntegerField(default=1)
    kategori = models.CharField(
        max_length=20,
        choices=[('ringan', 'Ringan'), ('sedang', 'Sedang'), ('berat', 'Berat')],
        default='ringan',
    )

    class Meta:
        verbose_name = 'Jenis pelanggaran'
        verbose_name_plural = 'Jenis pelanggaran'

    def __str__(self):
        return self.nama


class CatatanPelanggaran(models.Model):
    santri = models.ForeignKey(Santri, on_delete=models.CASCADE, related_name='pelanggaran')
    jenis = models.ForeignKey(JenisPelanggaran, on_delete=models.PROTECT)
    tanggal = models.DateField()
    pelapor = models.ForeignKey(Pegawai, on_delete=models.SET_NULL, null=True, blank=True)
    sanksi = models.CharField(max_length=200, blank=True)
    catatan = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Catatan pelanggaran'
        verbose_name_plural = 'Catatan pelanggaran'

    def __str__(self):
        return f'{self.santri} — {self.jenis}'


class AbsensiAsrama(models.Model):
    SESI = [
        ('malam', 'Malam'),
        ('shalat', 'Shalat'),
        ('pagi', 'Pagi'),
    ]
    STATUS = [
        ('hadir', 'Hadir'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
        ('alpa', 'Alpa'),
        ('terlambat', 'Terlambat'),
    ]
    santri = models.ForeignKey(Santri, on_delete=models.CASCADE, related_name='absensi_asrama')
    tanggal = models.DateField()
    sesi = models.CharField(max_length=20, choices=SESI, default='malam')
    status = models.CharField(max_length=20, choices=STATUS, default='hadir')
    petugas = models.ForeignKey(Pegawai, on_delete=models.SET_NULL, null=True, blank=True)
    catatan = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Absensi asrama'
        verbose_name_plural = 'Absensi asrama'
        unique_together = ('santri', 'tanggal', 'sesi')

    def __str__(self):
        return f'{self.santri} {self.tanggal} {self.sesi}'
