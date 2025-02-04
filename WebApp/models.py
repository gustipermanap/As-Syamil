from django.db import models
from django.core.validators import RegexValidator  # Tambahkan import ini
from django.contrib.auth.models import User  # Tambahkan import ini
from django.utils.text import slugify
#-------------------BASE------------------------

class SosialMedia(models.Model):
    title = models.CharField(max_length=25)
    url = models.URLField(max_length=100)
    icon = models.CharField(max_length=25)
    
    class Meta:
        verbose_name = "Sosial Media"
        verbose_name_plural = "Sosial Media"
    def __str__(self):
        return self.title

class DataSekolah(models.Model):
    nama_sekolah = models.CharField(max_length=100)
    alamat = models.TextField(max_length=100,blank=True, null=True)
    logo = models.ImageField(upload_to='logo/',blank=True, null=True)
    email = models.CharField(max_length=40)
    contact = models.CharField(max_length=20, validators=[RegexValidator(r'^\d+$', 'Hanya boleh diisi dengan angka')])
    open_hours = models.CharField(max_length=20, blank=True, null=True, default='Mon-Sat: 10AM - 5PM')
    class Meta:
        verbose_name = "Data Sekolah"
        verbose_name_plural = "Data Sekolah"
        ordering = ['-id']
#---------Heroes
    
class Hero(models.Model):
    welcome_text = models.CharField(max_length=100, default="Welcome to",blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    button_name=models.CharField(max_length=15,null=True,blank=True)
    image_landing_page = models.ImageField(upload_to='hero/',blank=True,null=True)
    primary_button_text = models.CharField(max_length=50, default="Watch Video",blank=True,null=True)
    primary_button_link = models.CharField(max_length=200, default="#about",blank=True,null=True)
    video_url = models.URLField(blank=True, null=True)
    video_button_text = models.CharField(max_length=50, default="Watch Video",blank=True,null=True)
    image = models.ImageField(upload_to='hero/',blank=True,null=True)
    image_alt = models.CharField(max_length=100,blank=True,null=True)
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"
        ordering = ['id']

class HeroBox(models.Model):
    icon = models.CharField(max_length=50, help_text="Bootstrap icon name (e.g. 'easel', 'gem')", null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = "Hero Box"
        verbose_name_plural = "Hero Box"

#-------------About-------------------------------------------------------------------------


class About(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    image_title = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='about/',blank=True,null=True)
    image_content= models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    image_video = models.ImageField(upload_to='about/',blank=True,null=True)
    Video_Url = models.CharField(max_length=200, null=True, blank=True, help_text="pilih salah satu antara video url atau video upload")
    video_upload = models.FileField(upload_to='about/',blank=True,null=True, help_text="pilih salah satu antara video url atau video upload")
    class Meta:
        verbose_name = "z About"
        verbose_name_plural = "z About"
        ordering = ['-id']
    def __str__(self):
        return self.title
    
class sponsor(models.Model):
    image = models.ImageField(upload_to='sponsor/',blank=True,null=True)
    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsor"

class CalltoAction(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    image_background = models.ImageField(upload_to='calltoaction/',blank=True,null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True, help_text="pilih salah satu antara video url atau video upload")
    video_upload = models.FileField(upload_to='calltoaction/',blank=True,null=True, help_text="pilih salah satu antara video url atau video upload")
    text_button = models.CharField(max_length=20, null=True, blank=True, default='#')
    class Meta:
        verbose_name = "Call to Action"
        verbose_name_plural = "Call to Action"
    def __str__(self):
        return self.title

#-------------Service-------------------------------------------------------------------------
class Service(models.Model):
    service_title = models.CharField(max_length=20, null=True, blank=True)
    service_description = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Service"
        ordering = ['-id']
    def __str__(self):
        return self.service_title
class Service_Item(models.Model):
    service_Item_title = models.CharField(max_length=20, null=True, blank=True)
    service_Item_description = models.CharField(max_length=200, null=True, blank=True)
    link_Item_service= models.CharField(max_length=200, null=True, blank=True, help_text="pilih salah satu antara video url atau video upload")
    image_service = models.ImageField(upload_to='service/',blank=True,null=True)
    class Meta:
        verbose_name = "Service Item"
        verbose_name_plural = "Service Item"
        ordering = ['-service_Item_title']
    def __str__(self):
        return self.service_Item_title
#-------------Testimonials-------------------------------------------------------------------------
class testimonial(models.Model):
    testimonial_title = models.CharField(max_length=20, null=True, blank=True)
    testimonial_description = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonial"
        ordering = ['-id']
    def __str__(self):
        return self.title
class testimonial_Item(models.Model):
    testimonial_image = models.ImageField(upload_to='testimonial/', null=True, blank=True)
    testimonial_Personal_title = models.CharField(max_length=20, null=True, blank=True)
    testimonial_Personal_departement = models.CharField(max_length=20, null=True, blank=True)
    testimonial_Personal_description = models.CharField(max_length=200, null=True, blank=True)
    #ink_Personal_testimonial= models.CharField(max_length=200, null=True, blank=True, help_text="pilih salah satu antara video url atau video upload")
    class Meta:
        verbose_name = "Testimonial Person"
        verbose_name_plural = "Testimonial Person"
    def __str__(self):
        return self.title
#-------------Portfolio-------------------------------------------------------------------------
class Portfolio(models.Model):
    portfolio_title = models.CharField(max_length=20, null=True, blank=True)
    portfolio_description = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolio"
        ordering = ['-id']
    def __str__(self):
        return self.portfolio_title
class Portfolio_tag(models.Model):
    portfolio_tag = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.portfolio_tag
class Portfolio_Item(models.Model):
    portfolio_image = models.ImageField(upload_to='portfolio/', null=True, blank=True)
    portfolio_Item_title = models.CharField(max_length=20, null=True, blank=True)
    portfolio_Item_description = models.CharField(max_length=200, null=True, blank=True)
    portfolio_tag = models.ForeignKey(Portfolio_tag, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name = "Portfolio Item"
    def __str__(self):
        return self.portfolio_Item_title
#-------------Team-------------------------------------------------------------------------
class Team(models.Model):
    title_team = models.CharField(max_length=20, null=True, blank=True)
    description_team = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = "Header Team"
        verbose_name_plural = "Header Team"
        ordering = ['-id']
    def __str__(self):
        return self.title_team
class Team_Member(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    team_image = models.ImageField(upload_to='team/', null=True, blank=True)
    team_Item_title = models.CharField(max_length=20, null=True, blank=True)
    team_Item_description = models.CharField(max_length=200, null=True, blank=True)
    link_Item_team= models.CharField(max_length=200, null=True, blank=True, help_text="pilih salah satu antara video url atau video upload")
    person_facebook_url = models.CharField(max_length=200, null=True, blank=True)
    person_twitter_url = models.CharField(max_length=200, null=True, blank=True)
    person_instagram_url = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = "Team Person"
        verbose_name_plural = "Team Person"
    def __str__(self):
        return self.title
#-------------Blog-------------------------------------------------------------------------
# class blog (models.Model):
#     title_blog = models.CharField(max_length=20, null=True, blank=True)
#     description_blog = models.CharField(max_length=200, null=True, blank=True)
#     class Meta:
#         verbose_name = "Blog"
#         verbose_name_plural = "Blog"
#         ordering = ['-id']
#     def __str__(self):
#         return self.title_blog

# class blog_detail(models.Model):
#     title = models.CharField(max_length=100, null=True, blank=True)
#     content = models.TextField(null=True, blank=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to='blog_details/', blank=True, null=True)
#     tags = models.ManyToManyField('blog', blank=True)
#     class Meta:
#         verbose_name = "Blog Detail"
#         verbose_name_plural = "Blog Details"
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.title

#-------------Contact-------------------------------------------------------------------------
class message_guest(models.Model):
    title_message= models.CharField(max_length=20, null=True, blank=True)
    description_for_message = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name = "Guest Message"
        verbose_name_plural = "Guest Message"
        ordering = ['-id']
    def __str__(self):
        return self.title_message
    
class message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
#-------------Pendaftaran-------------------------------------------------------------------------
# WebApp/models.py

class Pendaftaran(models.Model):
    # Data Calon Peserta Didik
    nama_lengkap = models.CharField(max_length=100)
    nik = models.CharField(max_length=16)
    jenis_kelamin_choices = [
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan'),
    ]
    jenis_kelamin = models.CharField(max_length=1, choices=jenis_kelamin_choices)
    nisn = models.CharField(max_length=12)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    agama = models.CharField(max_length=50)
    no_handphone = models.CharField(max_length=15)
    anak_ke = models.IntegerField()
    jumlah_saudara = models.IntegerField()

    # Data Pendidikan Sebelumnya
    asal_sekolah_choices = [
        ('SMP', 'SMP'),
        ('MTs', 'MTs'),
        ('Lainnya', 'Lainnya'),
    ]
    asal_sekolah = models.CharField(max_length=10, choices=asal_sekolah_choices)
    tgl_no_ijazah = models.DateField()
    lama_belajar = models.IntegerField()
    pindahan_dari_sekolah = models.CharField(max_length=100, blank=True, null=True)
    diterima_di_sekolah = models.DateField(blank=True, null=True)
    alasan_pindah = models.TextField(blank=True, null=True)

    # Alamat Lengkap
    alamat = models.TextField(blank=True, null=True)
    rt = models.CharField(max_length=10)
    rw = models.CharField(max_length=10)
    kelurahan = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    kota_kabupaten = models.CharField(max_length=100)
    kode_pos = models.CharField(max_length=10)

    # Data Orangtua/Wali
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

    # Foto Calon Siswa
    foto = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return self.nama_lengkap

    
    
    #=================blog=============
# class Post(models.Model):
#     title = models.CharField(max_length=100, blank=True, null=True)
#     slug = models.SlugField(unique=True, blank=True, null=True)  # Field slug
#     image = models.ImageField(upload_to='blog/', blank=True, null=True)
#     content = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)  # Membuat slug berdasarkan judul
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title
    
class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Field slug
    image = models.ImageField(upload_to='blog/', blank=True, null=True)  # Gambar untuk postingan
    content = models.TextField(blank=True, null=True)  # Konten postingan
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Penulis postingan
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal pembuatan
    updated_at = models.DateTimeField(auto_now=True)  # Tanggal pembaruan

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Membuat slug berdasarkan judul
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title