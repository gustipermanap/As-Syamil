from django.urls import path

from . import views

app_name = 'keuangan'

urlpatterns = [
    path('operasi/keuangan/', views.DaftarTagihan.as_view(), name='tagihan'),
    path('operasi/keuangan/jenis/baru/', views.TambahJenis.as_view(), name='jenis_baru'),
    path('operasi/keuangan/generate/', views.generate, name='generate'),
    path('operasi/keuangan/<int:pk>/bayar/', views.bayar, name='bayar'),
    path('operasi/keuangan/kwitansi/<int:pk>/', views.kwitansi, name='kwitansi'),
]
