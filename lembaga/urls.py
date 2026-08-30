from django.urls import path

from . import views

app_name = 'lembaga'

urlpatterns = [
    path('operasi/pengaturan/', views.UbahPengaturan.as_view(), name='pengaturan'),
    path('operasi/unit/', views.DaftarUnit.as_view(), name='unit'),
    path('operasi/unit/baru/', views.TambahUnit.as_view(), name='unit_baru'),
    path('operasi/jenjang/baru/', views.TambahJenjang.as_view(), name='jenjang_baru'),
    path('operasi/tahun-ajaran/', views.DaftarTahunAjaran.as_view(), name='tahun'),
    path('operasi/tahun-ajaran/baru/', views.TambahTahunAjaran.as_view(), name='tahun_baru'),
    path('operasi/periode/baru/', views.TambahPeriode.as_view(), name='periode_baru'),
]
