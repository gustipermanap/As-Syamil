from django.urls import path

from . import views

app_name = 'lembaga'

urlpatterns = [
    path('operasi/pengaturan/', views.UbahPengaturan.as_view(), name='pengaturan'),
    path('operasi/unit/', views.DaftarUnit.as_view(), name='unit'),
    path('operasi/unit/baru/', views.TambahUnit.as_view(), name='unit_baru'),
    path('operasi/unit/<int:pk>/ubah/', views.UbahUnit.as_view(), name='unit_ubah'),
    path('operasi/jenjang/baru/', views.TambahJenjang.as_view(), name='jenjang_baru'),
    path('operasi/jenjang/<int:pk>/ubah/', views.UbahJenjang.as_view(), name='jenjang_ubah'),
    path('operasi/tahun-ajaran/', views.DaftarTahunAjaran.as_view(), name='tahun'),
    path('operasi/tahun-ajaran/baru/', views.TambahTahunAjaran.as_view(), name='tahun_baru'),
    path('operasi/tahun-ajaran/<int:pk>/ubah/', views.UbahTahunAjaran.as_view(), name='tahun_ubah'),
    path('operasi/periode/baru/', views.TambahPeriode.as_view(), name='periode_baru'),
    path('operasi/periode/<int:pk>/ubah/', views.UbahPeriode.as_view(), name='periode_ubah'),
]
