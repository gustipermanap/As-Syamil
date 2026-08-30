from django.contrib.auth.models import Group

from .models import SEMUA_GRUP


def pastikan_grup():
    for nama in SEMUA_GRUP:
        Group.objects.get_or_create(name=nama)


def user_punya_grup(user, nama_list):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if isinstance(nama_list, str):
        nama_list = [nama_list]
    return user.groups.filter(name__in=nama_list).exists()
