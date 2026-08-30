from django.contrib import admin
from .models import Jenjang, Pengaturan, Periode, TahunAjaran, UnitPendidikan


@admin.register(Pengaturan)
class PengaturanAdmin(admin.ModelAdmin):
    list_display = ('nama_tampil', 'pengelola_keuangan', 'jenis_periode', 'portal_santri_aktif')


admin.site.register(UnitPendidikan)
admin.site.register(Jenjang)
admin.site.register(TahunAjaran)
admin.site.register(Periode)
