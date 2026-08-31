from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from lembaga.models import Pengaturan
from .models import GRUP_BENDAHARA, GRUP_MUDIR, GRUP_OPERASI, GRUP_SANTRI, GRUP_TU, GRUP_WALI
from .services import user_punya_grup


def respon_dilarang(request, pesan='Tidak berhak mengakses halaman ini.'):
    return render(request, 'pengguna/dilarang.html', {'pesan': pesan}, status=403)


class OperasiMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('pengguna:masuk')

    def test_func(self):
        return user_punya_grup(self.request.user, GRUP_OPERASI)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return respon_dilarang(self.request, 'Tidak berhak mengakses portal operasional.')
        return super().handle_no_permission()


class WaliMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('pengguna:masuk')

    def test_func(self):
        return user_punya_grup(self.request.user, [GRUP_WALI]) or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return respon_dilarang(self.request, 'Tidak berhak mengakses portal wali.')
        return super().handle_no_permission()


class SantriPortalMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('pengguna:masuk')

    def test_func(self):
        if not Pengaturan.get().portal_santri_aktif:
            return False
        return user_punya_grup(self.request.user, [GRUP_SANTRI]) or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return respon_dilarang(self.request, 'Portal santri tidak aktif atau Anda tidak berhak.')
        return super().handle_no_permission()


class KeuanganMixin(OperasiMixin):
    def test_func(self):
        if not user_punya_grup(self.request.user, GRUP_OPERASI):
            return False
        if user_punya_grup(self.request.user, [GRUP_MUDIR]):
            return True
        pengaturan = Pengaturan.get()
        if pengaturan.pengelola_keuangan == Pengaturan.PENGELOLA_TU:
            return user_punya_grup(self.request.user, [GRUP_TU])
        return user_punya_grup(self.request.user, [GRUP_BENDAHARA])

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return respon_dilarang(self.request, 'Menu keuangan hanya untuk pengelola yang ditunjuk.')
        return super().handle_no_permission()


def butuh_operasi(view):
    @login_required(login_url='/masuk/')
    @wraps(view)
    def inner(request, *args, **kwargs):
        if not user_punya_grup(request.user, GRUP_OPERASI):
            return respon_dilarang(request, 'Tidak berhak mengakses portal operasional.')
        return view(request, *args, **kwargs)
    return inner


def butuh_keuangan(view):
    @butuh_operasi
    @wraps(view)
    def inner(request, *args, **kwargs):
        if user_punya_grup(request.user, [GRUP_MUDIR]):
            return view(request, *args, **kwargs)
        pengaturan = Pengaturan.get()
        if pengaturan.pengelola_keuangan == Pengaturan.PENGELOLA_TU:
            if not user_punya_grup(request.user, [GRUP_TU]):
                return respon_dilarang(request, 'Menu keuangan dipegang Tata Usaha.')
        elif not user_punya_grup(request.user, [GRUP_BENDAHARA]):
            return respon_dilarang(request, 'Menu keuangan dipegang Bendahara.')
        return view(request, *args, **kwargs)
    return inner


def butuh_wali(view):
    @login_required(login_url='/masuk/')
    @wraps(view)
    def inner(request, *args, **kwargs):
        if not (user_punya_grup(request.user, [GRUP_WALI]) or request.user.is_superuser):
            return respon_dilarang(request, 'Tidak berhak mengakses portal wali.')
        return view(request, *args, **kwargs)
    return inner


def butuh_santri(view):
    @login_required(login_url='/masuk/')
    @wraps(view)
    def inner(request, *args, **kwargs):
        if not Pengaturan.get().portal_santri_aktif:
            return respon_dilarang(request, 'Portal santri tidak aktif.')
        if not (user_punya_grup(request.user, [GRUP_SANTRI]) or request.user.is_superuser):
            return respon_dilarang(request, 'Tidak berhak mengakses portal santri.')
        return view(request, *args, **kwargs)
    return inner
