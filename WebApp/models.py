from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify


class SosialMedia(models.Model):
    title = models.CharField(max_length=25)
    url = models.URLField(max_length=100)
    icon = models.CharField(max_length=25, help_text="Nama ikon Bootstrap Icons, contoh: facebook")

    class Meta:
        verbose_name = 'Sosial Media'
        verbose_name_plural = 'Sosial Media'

    def __str__(self):
        return self.title


class DataSekolah(models.Model):
    nama_sekolah = models.CharField(max_length=100)
    alamat = models.TextField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    email = models.CharField(max_length=40)
    contact = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\d+$', 'Hanya boleh diisi dengan angka')],
    )
    open_hours = models.CharField(max_length=40, blank=True, null=True, default='Senin-Sabtu: 07.00 - 16.00')
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Nomor WhatsApp angka saja, contoh: 6282128333839',
    )
    ppdb_periode = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Contoh: 1 Mei 2026 - 30 Juni 2026',
    )

    class Meta:
        verbose_name = 'Data Sekolah'
        verbose_name_plural = 'Data Sekolah'
        ordering = ['-id']

    def __str__(self):
        return self.nama_sekolah

    @property
    def whatsapp_url(self):
        raw = self.whatsapp or self.contact or ''
        digits = ''.join(ch for ch in raw if ch.isdigit())
        if digits.startswith('0'):
            digits = '62' + digits[1:]
        if not digits:
            digits = '6282128333839'
        return f'https://wa.me/{digits}'


class Hero(models.Model):
    welcome_text = models.CharField(max_length=100, default='Welcome to', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    button_name = models.CharField(max_length=15, null=True, blank=True)
    image_landing_page = models.ImageField(upload_to='hero/', blank=True, null=True)
    primary_button_text = models.CharField(max_length=50, default='Watch Video', blank=True, null=True)
    primary_button_link = models.CharField(max_length=200, default='#about', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_button_text = models.CharField(max_length=50, default='Watch Video', blank=True, null=True)
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    image_alt = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'
        ordering = ['id']

    def __str__(self):
        return self.title or f'Hero #{self.pk}'


class HeroBox(models.Model):
    icon = models.CharField(max_length=50, help_text="Nama ikon Bootstrap, contoh: easel", null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Hero Box'
        verbose_name_plural = 'Hero Box'

    def __str__(self):
        return self.title or f'Hero Box #{self.pk}'


class About(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    image_title = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    image_content = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    image_video = models.ImageField(upload_to='about/', blank=True, null=True)
    Video_Url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Isi URL video atau unggah file di bawah. Cukup salah satu.',
    )
    video_upload = models.FileField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'
        ordering = ['-id']

    def __str__(self):
        return self.title or f'About #{self.pk}'


class sponsor(models.Model):
    image = models.ImageField(upload_to='sponsor/', blank=True, null=True)

    class Meta:
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsor'

    def __str__(self):
        return f'Sponsor #{self.pk}'


class CalltoAction(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    image_background = models.ImageField(upload_to='calltoaction/', blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True, help_text='URL video atau tautan tombol')
    video_upload = models.FileField(upload_to='calltoaction/', blank=True, null=True)
    text_button = models.CharField(max_length=40, null=True, blank=True, default='Daftar Sekarang')

    class Meta:
        verbose_name = 'Call to Action'
        verbose_name_plural = 'Call to Action'

    def __str__(self):
        return self.title or f'CTA #{self.pk}'


class Service(models.Model):
    service_title = models.CharField(max_length=20, null=True, blank=True)
    service_description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'
        ordering = ['-id']

    def __str__(self):
        return self.service_title or f'Service #{self.pk}'


class Service_Item(models.Model):
    service_Item_title = models.CharField(max_length=20, null=True, blank=True)
    service_Item_description = models.CharField(max_length=200, null=True, blank=True)
    link_Item_service = models.CharField(max_length=200, null=True, blank=True)
    image_service = models.ImageField(upload_to='service/', blank=True, null=True)

    class Meta:
        verbose_name = 'Service Item'
        verbose_name_plural = 'Service Item'
        ordering = ['-service_Item_title']

    def __str__(self):
        return self.service_Item_title or f'Service Item #{self.pk}'


class testimonial(models.Model):
    testimonial_title = models.CharField(max_length=20, null=True, blank=True)
    testimonial_description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonial'
        ordering = ['-id']

    def __str__(self):
        return self.testimonial_title or f'Testimonial #{self.pk}'


class testimonial_Item(models.Model):
    testimonial_image = models.ImageField(upload_to='testimonial/', null=True, blank=True)
    testimonial_Personal_title = models.CharField(max_length=20, null=True, blank=True)
    testimonial_Personal_departement = models.CharField(max_length=20, null=True, blank=True)
    testimonial_Personal_description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Testimonial Person'
        verbose_name_plural = 'Testimonial Person'

    def __str__(self):
        return self.testimonial_Personal_title or f'Testimoni #{self.pk}'


class Portfolio(models.Model):
    portfolio_title = models.CharField(max_length=20, null=True, blank=True)
    portfolio_description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolio'
        ordering = ['-id']

    def __str__(self):
        return self.portfolio_title or f'Portfolio #{self.pk}'


class Portfolio_tag(models.Model):
    portfolio_tag = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.portfolio_tag or f'Tag #{self.pk}'


class Portfolio_Item(models.Model):
    portfolio_image = models.ImageField(upload_to='portfolio/', null=True, blank=True)
    portfolio_Item_title = models.CharField(max_length=20, null=True, blank=True)
    portfolio_Item_description = models.CharField(max_length=200, null=True, blank=True)
    portfolio_tag = models.ForeignKey(Portfolio_tag, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Portfolio Item'

    def __str__(self):
        return self.portfolio_Item_title or f'Portfolio Item #{self.pk}'


class Team(models.Model):
    title_team = models.CharField(max_length=20, null=True, blank=True)
    description_team = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Header Team'
        verbose_name_plural = 'Header Team'
        ordering = ['-id']

    def __str__(self):
        return self.title_team or f'Team #{self.pk}'


class Team_Member(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    team_image = models.ImageField(upload_to='team/', null=True, blank=True)
    team_Item_title = models.CharField(max_length=20, null=True, blank=True)
    team_Item_description = models.CharField(max_length=200, null=True, blank=True)
    link_Item_team = models.CharField(max_length=200, null=True, blank=True)
    person_facebook_url = models.CharField(max_length=200, null=True, blank=True)
    person_twitter_url = models.CharField(max_length=200, null=True, blank=True)
    person_instagram_url = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Team Person'
        verbose_name_plural = 'Team Person'

    def __str__(self):
        return self.team_Item_title or self.title or f'Anggota #{self.pk}'


class message_guest(models.Model):
    title_message = models.CharField(max_length=20, null=True, blank=True)
    description_for_message = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Guest Message'
        verbose_name_plural = 'Guest Message'
        ordering = ['-id']

    def __str__(self):
        return self.title_message or f'Header kontak #{self.pk}'


class message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pesan Tamu'
        verbose_name_plural = 'Pesan Tamu'
        ordering = ['-created_at']

    def __str__(self):
        return self.subject


class Pendaftaran(models.Model):
    jenis_kelamin_choices = [
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan'),
    ]
    asal_sekolah_choices = [
        ('SMP', 'SMP'),
        ('MTs', 'MTs'),
        ('Lainnya', 'Lainnya'),
    ]

    nama_lengkap = models.CharField(max_length=100)
    nik = models.CharField(max_length=16)
    jenis_kelamin = models.CharField(max_length=1, choices=jenis_kelamin_choices)
    nisn = models.CharField(max_length=12)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    agama = models.CharField(max_length=50)
    no_handphone = models.CharField(max_length=15)
    anak_ke = models.IntegerField()
    jumlah_saudara = models.IntegerField()
    asal_sekolah = models.CharField(max_length=10, choices=asal_sekolah_choices)
    tgl_no_ijazah = models.DateField()
    lama_belajar = models.IntegerField()
    pindahan_dari_sekolah = models.CharField(max_length=100, blank=True, null=True)
    diterima_di_sekolah = models.DateField(blank=True, null=True)
    alasan_pindah = models.TextField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    rt = models.CharField(max_length=10)
    rw = models.CharField(max_length=10)
    kelurahan = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    kota_kabupaten = models.CharField(max_length=100)
    kode_pos = models.CharField(max_length=10)
    nama_ayah = models.CharField(max_length=100)
    nama_ibu = models.CharField(max_length=100)
    pekerjaan_ayah = models.CharField(max_length=100)
    pekerjaan_ibu = models.CharField(max_length=100)
    pendidikan_ayah = models.CharField(max_length=50)
    pendidikan_ibu = models.CharField(max_length=50)
    penghasilan_bulanan = models.DecimalField(max_digits=10, decimal_places=2)
    ktp_ayah = models.BooleanField()
    ktp_ibu = models.BooleanField()
    alamat_orangtua = models.TextField()
    foto = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    gelombang = models.ForeignKey(
        'ppdb.GelombangPPDB',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pendaftar',
    )
    kode_pendaftaran = models.CharField(max_length=20, blank=True, unique=True, null=True)
    status = models.CharField(
        max_length=30,
        default='dikirim',
        choices=[
            ('dikirim', 'Dikirim'),
            ('berkas_kurang', 'Berkas kurang'),
            ('verifikasi', 'Verifikasi'),
            ('tes', 'Tes'),
            ('diterima', 'Diterima'),
            ('cadangan', 'Cadangan'),
            ('ditolak', 'Ditolak'),
            ('mengundurkan_diri', 'Mengundurkan diri'),
        ],
    )

    class Meta:
        verbose_name = 'Pendaftaran PPDB'
        verbose_name_plural = 'Pendaftaran PPDB'
        ordering = ['-id']

    def __str__(self):
        return self.nama_lengkap


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Berita / Blog'
        verbose_name_plural = 'Berita / Blog'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or f'Post #{self.pk}'
