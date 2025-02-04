from django.urls import path, include
from .views import base
from . import views
from .views import message_view, success_view, pendaftaran_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', base, name='admin'),
    path('', views.base, name='base'),
    # path('blog-detail/',views.dblog,name='details_blog'),
    path('login/', views.base, name='admin'),
    # path('blog/', blog_page, name='blog'), 
    path('contact/', message_view, name='contact'),
    path('success/', success_view, name='success'),
    path('ppdb/', pendaftaran_view, name='pendaftaran'),
    # path('/<slug:slug>/', views.blog, name ='blog'),
    
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:slug>/', views.post_detail, name='blog_detail'),  # Pastikan ini ada dan benar
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)