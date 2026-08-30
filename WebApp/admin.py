from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import (
    About,
    CalltoAction,
    DataSekolah,
    Hero,
    HeroBox,
    Pendaftaran,
    Portfolio,
    Portfolio_Item,
    Portfolio_tag,
    Post,
    Service,
    Service_Item,
    SosialMedia,
    Team,
    Team_Member,
    message,
    message_guest,
    sponsor,
    testimonial,
    testimonial_Item,
)


@admin.register(SosialMedia)
class SosialMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'url')


@admin.register(DataSekolah)
class DataSekolahAdmin(admin.ModelAdmin):
    list_display = ('nama_sekolah', 'email', 'contact', 'whatsapp', 'ppdb_periode')


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'welcome_text')


@admin.register(HeroBox)
class HeroBoxAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'icon')


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


@admin.register(CalltoAction)
class CalltoActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'text_button')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_title', 'service_description')


@admin.register(Service_Item)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('service_Item_title', 'service_Item_description')


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('portfolio_title', 'portfolio_description')


@admin.register(Portfolio_tag)
class PortfolioTagAdmin(admin.ModelAdmin):
    list_display = ('portfolio_tag',)


@admin.register(Portfolio_Item)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('portfolio_Item_title', 'portfolio_tag')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('title_team', 'description_team')


@admin.register(Team_Member)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team_Item_title', 'title')


@admin.register(testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('testimonial_title', 'testimonial_description')


@admin.register(testimonial_Item)
class TestimonialItemAdmin(admin.ModelAdmin):
    list_display = ('testimonial_Personal_title', 'testimonial_Personal_departement')


@admin.register(message_guest)
class MessageGuestAdmin(admin.ModelAdmin):
    list_display = ('title_message', 'description_for_message')


@admin.register(message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20})},
    }


@admin.register(Pendaftaran)
class PendaftaranAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'nik', 'nisn', 'no_handphone', 'created_at')
    search_fields = ('nama_lengkap', 'nik', 'nisn')
    list_filter = ('jenis_kelamin', 'agama', 'asal_sekolah')
    readonly_fields = ('created_at',)
