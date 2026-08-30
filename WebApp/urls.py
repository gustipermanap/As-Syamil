from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.message_view, name='contact'),
    path('success/', views.success_view, name='success'),
    path('ppdb/', views.pendaftaran_view, name='pendaftaran'),
    path('ppdb/sukses/', views.pendaftaran_sukses_view, name='pendaftaran_sukses'),
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:slug>/', views.post_detail, name='blog_detail'),
]
