# WebApp/views.py
from django.shortcuts import render
from .models import Post  # Menggunakan model Post yang benar

def blog_page(request):
    blogg = Post.objects.all()  # Mengambil semua data dari model Post
    return render(request, 'WebApp/pages/blog.html', {'blogg': blogg, 'additional_context': 'value'})
