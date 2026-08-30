from django.conf import settings
from django.db import models

GRUP_MUDIR = 'mudir'
GRUP_TU = 'tata_usaha'
GRUP_BENDAHARA = 'bendahara'
GRUP_USTADZ = 'ustadz'
GRUP_MUSYRIF = 'musyrif'
GRUP_WALI = 'wali'
GRUP_SANTRI = 'santri'

SEMUA_GRUP = [
    GRUP_MUDIR,
    GRUP_TU,
    GRUP_BENDAHARA,
    GRUP_USTADZ,
    GRUP_MUSYRIF,
    GRUP_WALI,
    GRUP_SANTRI,
]

GRUP_OPERASI = [GRUP_MUDIR, GRUP_TU, GRUP_BENDAHARA, GRUP_USTADZ, GRUP_MUSYRIF]


class Profil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil')
    telepon = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Profil pengguna'
        verbose_name_plural = 'Profil pengguna'

    def __str__(self):
        return self.user.get_username()

    def nama_grup(self):
        return list(self.user.groups.values_list('name', flat=True))
