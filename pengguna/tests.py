from django.test import TestCase
from django.urls import reverse

from lembaga.factories import buat_user, data_dasar
from lembaga.models import Pengaturan


class PortalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        data_dasar()
        cls.tu = buat_user('tu_portal', 'tata_usaha')
        cls.wali = buat_user('wali_portal', 'wali')
        cls.ustadz = buat_user('ustadz_portal', 'ustadz')
        cls.santri = buat_user('santri_portal', 'santri')

    def test_masuk_bukan_beranda(self):
        self.assertEqual(reverse('pengguna:masuk'), '/masuk/')
        r = self.client.get('/masuk/')
        self.assertEqual(r.status_code, 200)

    def test_tu_masuk_operasi(self):
        self.client.login(username='tu_portal', password='sandi123')
        r = self.client.get(reverse('pengguna:operasi'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Santri aktif')

    def test_wali_ditolak_operasi(self):
        self.client.login(username='wali_portal', password='sandi123')
        r = self.client.get(reverse('pengguna:operasi'))
        self.assertEqual(r.status_code, 403)
        self.assertContains(r, 'Tidak berhak', status_code=403)
        self.assertContains(r, 'portal wali', status_code=403)

    def test_wali_masuk_portal_wali(self):
        self.client.login(username='wali_portal', password='sandi123')
        r = self.client.get(reverse('pengguna:wali'))
        self.assertEqual(r.status_code, 200)

    def test_ustadz_tidak_lihat_menu_keuangan(self):
        self.client.login(username='ustadz_portal', password='sandi123')
        r = self.client.get(reverse('pengguna:operasi'))
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, reverse('keuangan:tagihan'))
        r2 = self.client.get(reverse('keuangan:tagihan'))
        self.assertEqual(r2.status_code, 403)
        self.assertContains(r2, 'keuangan', status_code=403)

    def test_portal_santri_bendera(self):
        p = Pengaturan.get()
        p.portal_santri_aktif = False
        p.save()
        self.client.login(username='santri_portal', password='sandi123')
        r = self.client.get(reverse('pengguna:santri'))
        self.assertEqual(r.status_code, 403)
        p.portal_santri_aktif = True
        p.save()
        r = self.client.get(reverse('pengguna:santri'))
        self.assertEqual(r.status_code, 200)

    def test_redirect_login_wali(self):
        r = self.client.post(reverse('pengguna:masuk'), {
            'username': 'wali_portal', 'password': 'sandi123',
        })
        self.assertRedirects(r, reverse('pengguna:wali'))
