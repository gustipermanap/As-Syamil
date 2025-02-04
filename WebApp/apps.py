from django.apps import AppConfig


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WebApp'
    verbose_name='Content Management System'
# from django.apps import AppConfig
# from django.contrib.admin import site
# from .models import (
#     SosialMedia, DataSekolah, Hero, HeroBox, About, sponsor,
#     CalltoAction, Service, Service_Item, testimonial, testimonial_Item,
#     Portfolio, Portfolio_tag, Portfolio_Item, Team, Team_Member,
#     Post, message_guest, message, Pendaftaran
# )

# class WebappConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    # name = 'WebApp'
    # verbose_name = 'Content Management System'

    # def ready(self):
    #     # Mengatur urutan model di admin
    #     site._registry[Hero].model._meta.ordering = ['-id'] 
    #     site._registry[SosialMedia].model._meta.ordering = ['-id']
    #     site._registry[DataSekolah].model._meta.ordering = ['-id'] # Hero tampil di atas
    #     site._registry[HeroBox].model._meta.ordering = ['-id']
    #     site._registry[About].model._meta.ordering = ['-id']  # About tampil di bawah Hero
    #     site._registry[sponsor].model._meta.ordering = ['-id']
    #     site._registry[CalltoAction].model._meta.ordering = ['-id']
    #     site._registry[Service].model._meta.ordering = ['-id']
    #     site._registry[Service_Item].model._meta.ordering = ['-id']
    #     site._registry[testimonial].model._meta.ordering = ['-id']
    #     site._registry[testimonial_Item].model._meta.ordering = ['-id']
    #     site._registry[Portfolio].model._meta.ordering = ['-id']
    #     site._registry[Portfolio_tag].model._meta.ordering = ['-id']
    #     site._registry[Portfolio_Item].model._meta.ordering = ['-id']
    #     site._registry[Team].model._meta.ordering = ['-id']
    #     site._registry[Team_Member].model._meta.ordering = ['-id']
    #     site._registry[Post].model._meta.ordering = ['-id']
    #     site._registry[message_guest].model._meta.ordering = ['-id']
    #     site._registry[message].model._meta.ordering = ['-id']
    #     site._registry[Pendaftaran].model._meta.ordering = ['-id']