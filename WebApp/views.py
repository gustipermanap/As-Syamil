from django.shortcuts import render, redirect
from .models import Post, SosialMedia, DataSekolah, Hero, HeroBox, About, sponsor, CalltoAction, Service, Service_Item, Team, Team_Member, message_guest, Portfolio, Portfolio_tag, Portfolio_Item
from . import models
from .forms import MessageForm, PendaftaranForm
from django.shortcuts import render, get_object_or_404


def blog_page(request):
    return render(request, 'pages/blog.html')

#----------------------------------------------------------------------
def base(request):
    sosmed = SosialMedia.objects.all()
    datas = DataSekolah.objects.all()
    heroes = Hero.objects.all()[:1]
    hbox = HeroBox.objects.all()[:4]
    about = About.objects.all()
    party = sponsor.objects.all()
    cta = CalltoAction.objects.all()
    service = Service.objects.all()
    service_item = Service_Item.objects.all()[:6]
    testimonial = models.testimonial.objects.all()
    testimonial_person = models.testimonial_Item.objects.all()
    team = Team.objects.all()
    team_Member = Team_Member.objects.all()
    port = models.Portfolio.objects.all()
    Porttag = models.Portfolio_tag.objects.all()
    port_item = models.Portfolio_Item.objects.all()[:6]
    mguest = message_guest.objects.all()
    
    context = {
        'sosmed': sosmed,
        'datas': datas,
        'heroes': heroes,
        'hbox' : hbox,
        'about' : about,
        'party' : party,
        'cta'   : cta,
        'service' : service,
        'service_item' : service_item,
        'team' : team,
        'team_Member' : team_Member,
        'testimonial': testimonial,
        'testimonial_person': testimonial_person,
        'port': port,
        'port_item': port_item,
        'Porttag' : Porttag,
        'mguest' : mguest,
    }
    return render(request, 'base.html', context)

# def Team_Member(request):
#     team_Member = Team_Member.objects.all()
#     return render(request, 'pages/team.html')

#
def service_detail(request):
    return render(request, 'pages/service-details.html')

# def portfolio_view(request):
#     portfolios = models.Portfolio.objects.all()  # Ambil semua data portfolio
#     portfolio_tags = models.Portfolio_tag.objects.all()  # Ambil semua tag portfolio
#     portfolio_items = models.Portfolio_Item.objects.all()  # Ambil semua item portfolio
       
#     context = {
#         'Portfolio': portfolios,
#         'Portfolio_tag': portfolio_tags,
#         'Portfolio_Item': portfolio_items,
#     }
#     return render(request, 'pages/portfolio.html', context)


def message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Ganti dengan URL yang sesuai
    else:
        form = MessageForm()
        # Mengisi form dengan data pengguna yang sedang login
        if request.user.is_authenticated:
            form.fields['name'].initial = request.user.get_full_name()  # Mengisi nama
            form.fields['email'].initial = request.user.email  # Mengisi email

    return render(request, 'pages/contact.html', {'form': form})

def success_view(request):
    return render(request, 'base.html')

# WebApp/views.py

# def ppdb_view(request):
#     if request.method == 'POST':
#         form = PPDBForm(request.POST, request.FILES)  # Tambahkan request.FILES untuk menangani file
#         if form.is_valid():
#             form.save()  # Simpan data pendaftaran ke model PPDB
#             return redirect('success')  # Ganti dengan URL yang sesuai
#     else:
#         form = PPDBForm()

#     return render(request, 'pages/ppdb.html', {'form': form})


# def ppdb_view(request):
#     if request.method == 'POST':
#         form = PPDBForm(request.POST, request.FILES)  # Handle file uploads too
#         if form.is_valid():
#             # Save the form data to the database if valid
#             form.save()
#             # After saving, you can redirect the user to a success page
#             return redirect('success')  # Change 'success_url' to an appropriate URL or named URL pattern
#     else:
#         form = PPDBForm()  # Create an empty form for GET requests
    
#     # Render the template with the form context
#     return render(request, 'pages/ppdb.html', {'form': form})

def pendaftaran_view(request):
    if request.method == 'POST':
        form = PendaftaranForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pendaftaran_sukses')  # Halaman setelah pendaftaran sukses
    else:
        form = PendaftaranForm()
    
    return render(request, 'pages/ppdb.html', {'form': form})



def post_list(request):
    # Mengambil 4 postingan terbaru
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'pages/blog.html', {'posts': posts})

def post_detail(request, slug):
    # Menampilkan detail postingan berdasarkan slug
    post = get_object_or_404(Post, slug=slug)  # Mengambil postingan berdasarkan slug
    return render(request, 'blog-details.html', {'post': post})  # Mengirimkan objek post ke template