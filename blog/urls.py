from django.urls import path
from . import views

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    # path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('', views.blog_page, name='blog_page'),
]
