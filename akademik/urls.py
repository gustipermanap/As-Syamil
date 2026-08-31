from django.urls import path

from . import views

app_name = 'akademik'

urlpatterns = [
    path('operasi/rb/', views.DaftarRB.as_view(), name='rb'),
    path('operasi/rb/baru/', views.TambahRB.as_view(), name='rb_baru'),
    path('operasi/rb/ruang/baru/', views.TambahRuang.as_view(), name='ruang_baru'),
    path('operasi/rb/ruang/<int:pk>/ubah/', views.UbahRuang.as_view(), name='ruang_ubah'),
    path('operasi/rb/<int:pk>/', views.DetailRB.as_view(), name='rb_detail'),
    path('operasi/rb/<int:pk>/ubah/', views.UbahRB.as_view(), name='rb_ubah'),
    path('operasi/rb/<int:pk>/anggota/', views.anggota_rb, name='rb_anggota'),
    path('operasi/rb/<int:pk>/pengampu/', views.pengampu_rb, name='rb_pengampu'),
    path('operasi/rb/<int:pk>/mapel/', views.pasang_mapel, name='rb_mapel'),
    path('operasi/mapel/', views.DaftarMapel.as_view(), name='mapel'),
    path('operasi/mapel/baru/', views.TambahMapel.as_view(), name='mapel_baru'),
    path('operasi/mapel/<int:pk>/ubah/', views.UbahMapel.as_view(), name='mapel_ubah'),
    path('operasi/jadwal/', views.DaftarJadwal.as_view(), name='jadwal'),
    path('operasi/jadwal/baru/', views.TambahJadwal.as_view(), name='jadwal_baru'),
    path('operasi/jadwal/<int:pk>/ubah/', views.UbahJadwal.as_view(), name='jadwal_ubah'),
    path('operasi/absensi/', views.DaftarPertemuan.as_view(), name='absensi'),
    path('operasi/absensi/baru/', views.TambahPertemuan.as_view(), name='pertemuan_baru'),
    path('operasi/absensi/<int:pk>/', views.isi_absensi, name='isi_absensi'),
    path('operasi/nilai/', views.DaftarNilai.as_view(), name='nilai'),
    path('operasi/nilai/baru/', views.TambahNilai.as_view(), name='nilai_baru'),
    path('operasi/nilai/<int:pk>/ubah/', views.UbahNilai.as_view(), name='nilai_ubah'),
    path('operasi/rekap-absensi/', views.RekapAbsensi.as_view(), name='rekap_absensi'),
    path('operasi/rb/<int:pk>/salin/', views.salin_rb_view, name='rb_salin'),
]
