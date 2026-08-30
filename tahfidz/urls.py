from django.urls import path

from . import views

app_name = 'tahfidz'

urlpatterns = [
    path('operasi/setoran/', views.DaftarSetoran.as_view(), name='setoran'),
    path('operasi/setoran/baru/', views.TambahSetoran.as_view(), name='setoran_baru'),
]
