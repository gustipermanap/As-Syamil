from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import MessageForm, PendaftaranForm
from .models import (
    About,
    CalltoAction,
    Portfolio,
    Portfolio_Item,
    Portfolio_tag,
    Post,
    Service,
    Service_Item,
    Team,
    Team_Member,
    HeroBox,
    message_guest,
    sponsor,
    testimonial,
    testimonial_Item,
)
from django.shortcuts import get_object_or_404

from ppdb.models import gelombang_berikutnya, gelombang_terbuka
from ppdb.services import buat_kode


def home(request):
    context = {
        'hbox': HeroBox.objects.all()[:4],
        'about': About.objects.all(),
        'party': sponsor.objects.all(),
        'cta_list': CalltoAction.objects.all(),
        'service': Service.objects.all(),
        'service_item': Service_Item.objects.all()[:6],
        'testimonial': testimonial.objects.all(),
        'testimonial_Item': testimonial_Item.objects.all(),
        'team': Team.objects.all(),
        'team_Member': Team_Member.objects.all(),
        'port': Portfolio.objects.all(),
        'Porttag': Portfolio_tag.objects.all(),
        'port_item': Portfolio_Item.objects.all()[:6],
        'recent_posts': Post.objects.all().order_by('-created_at')[:3],
        'mguest': message_guest.objects.all()[:1],
    }
    return render(request, 'base.html', context)


def message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pesan Anda sudah terkirim. Terima kasih.')
            return redirect('success')
        messages.error(request, 'Periksa kembali isian formulir.')
    else:
        form = MessageForm()
        if request.user.is_authenticated:
            form.fields['name'].initial = request.user.get_full_name() or request.user.username
            form.fields['email'].initial = request.user.email

    return render(request, 'pages/contact.html', {
        'form': form,
        'mguest': message_guest.objects.order_by('-id').first(),
    })


def success_view(request):
    return render(request, 'pages/success.html', {
        'page_title': 'Pesan terkirim',
        'page_text': 'Terima kasih. Pesan Anda sudah kami terima dan akan ditindaklanjuti.',
        'back_url_name': 'contact',
        'back_label': 'Kembali ke kontak',
    })


def pendaftaran_view(request):
    gelombang = gelombang_terbuka()
    berikutnya = None if gelombang else gelombang_berikutnya()
    if request.method == 'POST':
        if not gelombang:
            messages.error(request, 'Pendaftaran ditutup.')
            return render(request, 'pages/ppdb.html', {
                'form': None, 'gelombang': None, 'ditutup': True, 'berikutnya': berikutnya,
            })
        form = PendaftaranForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.gelombang = gelombang
            obj.status = 'dikirim'
            obj.kode_pendaftaran = buat_kode()
            obj.save()
            messages.success(request, f'Pendaftaran terkirim. Kode Anda: {obj.kode_pendaftaran}')
            return redirect('pendaftaran_sukses')
        messages.error(request, 'Periksa kembali isian formulir PPDB.')
    else:
        form = PendaftaranForm() if gelombang else None
    return render(request, 'pages/ppdb.html', {
        'form': form,
        'gelombang': gelombang,
        'ditutup': gelombang is None,
        'berikutnya': berikutnya,
    })


def pendaftaran_sukses_view(request):
    return render(request, 'pages/success.html', {
        'page_title': 'Pendaftaran terkirim',
        'page_text': 'Simpan kode pendaftaran yang tampil di notifikasi untuk cek status.',
        'back_url_name': 'home',
        'back_label': 'Kembali ke beranda',
    })


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pages/blog.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog-details.html', {'post': post})
