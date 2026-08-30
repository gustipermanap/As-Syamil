from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from kesiswaan.models import Santri
from lembaga.factories import buat_user


class RilisOperasionalTests(TestCase):
    def test_seed_dan_alur_dasar(self):
        call_command('seed_operasi', stdout=StringIO())
        self.assertGreaterEqual(Santri.objects.filter(status='aktif').count(), 5)
        self.client.login(username='mudir', password='sandi123')
        dasbor = self.client.get(reverse('pengguna:operasi'))
        self.assertEqual(dasbor.status_code, 200)
        self.assertEqual(dasbor.context['santri_aktif'], 5)
        self.client.logout()
        self.client.login(username='wali1', password='sandi123')
        wali = self.client.get(reverse('pengguna:wali'))
        self.assertEqual(wali.status_code, 200)
        self.assertContains(wali, 'Ahmad Zaki')
        self.assertNotContains(wali, 'Fatimah Azzahra')
        self.client.logout()
        self.client.login(username='ustadz1', password='sandi123')
        self.assertEqual(self.client.get(reverse('akademik:jadwal')).status_code, 200)
        self.assertEqual(self.client.get(reverse('keuangan:tagihan')).status_code, 403)
        self.client.logout()
        self.client.login(username='bendahara', password='sandi123')
        self.assertEqual(self.client.get(reverse('keuangan:tagihan')).status_code, 200)
        buat_user('check', 'tata_usaha')  # pastikan grup tetap ada
