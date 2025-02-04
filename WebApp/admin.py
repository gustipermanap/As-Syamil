from django.contrib import admin

from .models import Pendaftaran, Post, SosialMedia, DataSekolah, Hero, HeroBox, About, sponsor, CalltoAction, Service, Service_Item, testimonial, testimonial_Item, Portfolio, Portfolio_tag, Portfolio_Item, Team, Team_Member, message_guest
 
 
admin.site.site_header = "As-Syamil"  # Ganti dengan nama yang diinginkan
admin.site.site_title = "As-Syamil"   # Ganti dengan judul yang diinginkan
admin.site.index_title = "Selamat Datang di Admin As-Syamil"  # Ganti dengan judul yang diinginkan

 
@admin.register(SosialMedia)
class SosialMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'url')
    
@admin.register(DataSekolah)
class DataSekolahAdmin(admin.ModelAdmin):
    list_display = ('nama_sekolah', 'alamat', 'email', 'contact')
     
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'welcome_text')

@admin.register(HeroBox)
class HeroBoxAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'icon')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')

@admin.register(sponsor)
class sponsorAdmin(admin.ModelAdmin):
    list_display = ('image',)

@admin.register(CalltoAction)
class CalltoActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'link')
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_title', 'service_description')
    
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('portfolio_title', 'portfolio_description')  # Tambahkan fields yang diinginkan

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('title_team','description_team')  # Tambahkan fields yang diinginkan
    
# class PPDBAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'contact_number', 'parent_name', 'registration_date', 'date_of_birth')  # Fields to display in list view
#     search_fields = ('name', 'email', 'contact_number', 'parent_name')  # Fields to search by in the admin interface
#     list_filter = ('registration_date', 'date_of_birth')  # Filters for the admin interface
#     ordering = ('-registration_date',)  # Default ordering in the admin



class PostAdmin(admin.ModelAdmin):
    # Menampilkan fields yang diinginkan di admin panel
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}  # Mengisi slug otomatis berdasarkan title

class PendaftaranAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'nik', 'nisn', 'tempat_lahir', 'tanggal_lahir', 'agama')
    search_fields = ('nama_lengkap', 'nik', 'nisn')
    list_filter = ('jenis_kelamin', 'agama')
    
# admin.site.register(Hero)
# admin.site.register(HeroBox)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Pendaftaran, PendaftaranAdmin)
# # admin.site.register(PPDB, PPDBAdmin)
# admin.site.register(Service_Item)
# admin.site.register(testimonial)
# admin.site.register(testimonial_Item)
# admin.site.register(Portfolio)
# admin.site.register(Portfolio_tag)
# admin.site.register(Portfolio_Item)
# admin.site.register(Team)
# admin.site.register(Team_Member)
# # admin.site.register(blog)
# # admin.site.register(blog_detail)
# admin.site.register(message_guest)

admin.site.register(message_guest)
admin.site.register(Pendaftaran, PendaftaranAdmin)
admin.site.register(Portfolio_Item)
admin.site.register(Portfolio_tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Service_Item)
admin.site.register(Team_Member)
admin.site.register(testimonial)
admin.site.register(testimonial_Item)



# ========================================================
