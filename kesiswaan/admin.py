from django.contrib import admin
from .models import (
    AbsensiAsrama, CatatanPelanggaran, Gedung, Izin, JenisPelanggaran, Kamar,
    Pegawai, PenempatanKamar, Santri, WaliSantri,
)

admin.site.register(Pegawai)
admin.site.register(WaliSantri)
admin.site.register(Santri)
admin.site.register(Gedung)
admin.site.register(Kamar)
admin.site.register(PenempatanKamar)
admin.site.register(Izin)
admin.site.register(JenisPelanggaran)
admin.site.register(CatatanPelanggaran)
admin.site.register(AbsensiAsrama)
