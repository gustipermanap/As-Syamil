from django.urls import path

from . import views

app_name = 'ppdb'

urlpatterns = [
    path('operasi/ppdb/', views.AntrianPPDB.as_view(), name='antrian'),
    path('operasi/ppdb/gelombang/', views.DaftarGelombang.as_view(), name='gelombang'),
    path('operasi/ppdb/gelombang/baru/', views.TambahGelombang.as_view(), name='gelombang_baru'),
    path('operasi/ppdb/gelombang/<int:pk>/', views.UbahGelombang.as_view(), name='gelombang_ubah'),
    path('operasi/ppdb/gelombang/<int:pk>/status/<str:status>/', views.status_gelombang, name='gelombang_status'),
    path('operasi/ppdb/<int:pk>/jadikan/', views.jadikan_santri, name='jadikan'),
    path('operasi/ppdb/<int:pk>/<str:status>/', views.ubah_status, name='ubah_status'),
    path('ppdb/status/', views.cek_status, name='cek_status'),
]
