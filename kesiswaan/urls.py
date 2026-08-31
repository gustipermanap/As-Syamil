from django.urls import path

from . import views

app_name = 'kesiswaan'

urlpatterns = [
    path('operasi/santri/', views.DaftarSantri.as_view(), name='santri'),
    path('operasi/santri/baru/', views.TambahSantri.as_view(), name='santri_baru'),
    path('operasi/santri/<int:pk>/', views.DetailSantri.as_view(), name='santri_detail'),
    path('operasi/santri/<int:pk>/ubah/', views.UbahSantri.as_view(), name='santri_ubah'),
    path('operasi/wali/baru/', views.TambahWali.as_view(), name='wali_baru'),
    path('operasi/wali/<int:pk>/ubah/', views.UbahWali.as_view(), name='wali_ubah'),
    path('operasi/pegawai/', views.DaftarPegawai.as_view(), name='pegawai'),
    path('operasi/pegawai/baru/', views.TambahPegawai.as_view(), name='pegawai_baru'),
    path('operasi/pegawai/<int:pk>/ubah/', views.UbahPegawai.as_view(), name='pegawai_ubah'),
    path('operasi/pegawai/<int:pk>/status/', views.nonaktifkan_pegawai, name='pegawai_status'),
    path('operasi/asrama/', views.AsramaDasbor.as_view(), name='asrama'),
    path('operasi/asrama/gedung/baru/', views.TambahGedung.as_view(), name='gedung_baru'),
    path('operasi/asrama/gedung/<int:pk>/ubah/', views.UbahGedung.as_view(), name='gedung_ubah'),
    path('operasi/asrama/kamar/baru/', views.TambahKamar.as_view(), name='kamar_baru'),
    path('operasi/asrama/kamar/<int:pk>/ubah/', views.UbahKamar.as_view(), name='kamar_ubah'),
    path('operasi/asrama/penempatan/baru/', views.TambahPenempatan.as_view(), name='penempatan_baru'),
    path('operasi/izin/', views.DaftarIzin.as_view(), name='izin'),
    path('operasi/izin/baru/', views.TambahIzin.as_view(), name='izin_baru'),
    path('operasi/izin/<int:pk>/<str:aksi>/', views.aksi_izin, name='izin_aksi'),
    path('operasi/pelanggaran/', views.DaftarPelanggaran.as_view(), name='pelanggaran'),
    path('operasi/pelanggaran/baru/', views.TambahPelanggaran.as_view(), name='pelanggaran_baru'),
    path('operasi/pelanggaran/jenis/baru/', views.TambahJenisPelanggaran.as_view(), name='jenis_pelanggaran_baru'),
    path('wali/izin/', views.izin_wali, name='izin_wali'),
    path('santri/izin/', views.izin_santri, name='izin_santri'),
    path('operasi/asrama/absensi/', views.absensi_asrama, name='absensi_asrama'),
    path('operasi/asrama/pindah/', views.pindah_kamar_view, name='pindah_kamar'),
]
