"""URL utama proyek As-Syamil."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'As-Syamil'
admin.site.site_title = 'As-Syamil'
admin.site.index_title = 'Selamat datang di CMS As-Syamil'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', include('pengguna.urls')),
    path('', include('ppdb.urls')),
    path('', include('lembaga.urls')),
    path('', include('kesiswaan.urls')),
    path('', include('akademik.urls')),
    path('', include('tahfidz.urls')),
    path('', include('keuangan.urls')),
    path('', include('WebApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
