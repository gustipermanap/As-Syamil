from django.contrib import admin
from .models import (
    Absensi, JadwalSlot, KeanggotaanRB, KitabAtauMapel, MapelRB,
    Penilaian, PengampuRB, Pertemuan, RombonganBelajar, RuangBelajar,
)

for model in (
    RuangBelajar, RombonganBelajar, PengampuRB, KeanggotaanRB,
    KitabAtauMapel, MapelRB, JadwalSlot, Pertemuan, Absensi, Penilaian,
):
    admin.site.register(model)
