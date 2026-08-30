"""Data identitas sekolah untuk header, footer, dan WhatsApp di semua halaman."""
from .models import DataSekolah, Hero, SosialMedia


def site_identity(request):
    sekolah = DataSekolah.objects.order_by('-id').first()
    return {
        'sekolah': sekolah,
        'datas': DataSekolah.objects.order_by('-id')[:1],
        'sosmed': SosialMedia.objects.all(),
        'heroes': Hero.objects.all()[:1],
    }
