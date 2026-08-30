from django.contrib import admin
from .models import JenisTagihan, Pembayaran, Tagihan
from .services import terima_bayar


admin.site.register(JenisTagihan)
admin.site.register(Tagihan)


@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = ('nomor_kwitansi', 'tagihan', 'jumlah', 'tanggal')

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
        obj.tagihan.refresh_status()
