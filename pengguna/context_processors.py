from django.db.utils import OperationalError, ProgrammingError

from lembaga.models import Pengaturan, UnitPendidikan
from .models import GRUP_BENDAHARA, GRUP_MUDIR, GRUP_OPERASI, GRUP_SANTRI, GRUP_TU, GRUP_WALI
from .services import user_punya_grup


def _unit_aktif(tipe):
    qs = UnitPendidikan.objects.filter(tipe=tipe)
    if not qs.exists():
        return True
    return qs.filter(aktif=True).exists()


def menu_flags(user=None):
    p = Pengaturan.get()
    flags = {
        'ppdb': p.modul_ppdb,
        'akademik': p.modul_akademik and (_unit_aktif('formal') or _unit_aktif('diniyah')),
        'tahfidz': p.modul_tahfidz and _unit_aktif('tahfidz'),
        'asrama': p.modul_asrama and _unit_aktif('asrama'),
        'keuangan': p.modul_keuangan,
        'kedisiplinan': p.modul_kedisiplinan,
    }
    if user is not None:
        flags['boleh_keuangan'] = flags['keuangan'] and (
            user_punya_grup(user, [GRUP_MUDIR])
            or (
                user_punya_grup(user, [GRUP_TU])
                if p.pengelola_keuangan == Pengaturan.PENGELOLA_TU
                else user_punya_grup(user, [GRUP_BENDAHARA])
            )
        )
        flags['operasi'] = user_punya_grup(user, GRUP_OPERASI)
        flags['wali'] = user_punya_grup(user, [GRUP_WALI])
        flags['santri'] = user_punya_grup(user, [GRUP_SANTRI]) and p.portal_santri_aktif
    return flags


def portal_menu(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {}
    try:
        p = Pengaturan.get()
    except (OperationalError, ProgrammingError, Exception):
        return {}
    return {
        'pengaturan': p,
        'menu': menu_flags(request.user),
        'notif_belum': _hitung_notif(request.user),
    }


def _hitung_notif(user):
    try:
        from .models import Notifikasi
        return Notifikasi.objects.filter(penerima=user, dibaca=False).count()
    except (OperationalError, ProgrammingError, Exception):
        return 0
