from django.contrib import admin
from .models import ProgressHafalan, SetoranHafalan


@admin.register(SetoranHafalan)
class SetoranAdmin(admin.ModelAdmin):
    list_display = ('santri', 'jenis', 'mutu', 'tanggal')


admin.site.register(ProgressHafalan)
