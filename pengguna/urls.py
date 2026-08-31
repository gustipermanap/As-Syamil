from django.urls import path

from . import views

app_name = 'pengguna'

urlpatterns = [
    path('masuk/', views.masuk, name='masuk'),
    path('keluar/', views.keluar, name='keluar'),
    path('operasi/', views.OperasiDasbor.as_view(), name='operasi'),
    path('wali/', views.WaliDasbor.as_view(), name='wali'),
    path('santri/', views.SantriDasbor.as_view(), name='santri'),
    path('rapor/<int:santri_id>/', views.rapor_html, name='rapor'),
    path('notifikasi/', views.daftar_notifikasi, name='notifikasi'),
    path('privasi/', views.privasi, name='privasi'),
    path('operasi/pengguna/', views.DaftarPengguna.as_view(), name='daftar'),
    path('operasi/pengguna/<int:pk>/sandi/', views.reset_sandi, name='reset_sandi'),
]
