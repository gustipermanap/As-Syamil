from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from lembaga.factories import buat_user, data_dasar
from ppdb.models import GelombangPPDB, gelombang_terbuka
from ppdb.services import terima_menjadi_santri
from kesiswaan.models import Santri
from WebApp.models import Pendaftaran
from WebApp.tests import _ppdb_payload


def _gelombang(**kwargs):
    now = timezone.now()
    data = dict(
        nama='Gelombang tes',
        mulai=now - timedelta(days=1),
        selesai=now + timedelta(days=10),
        kuota=10,
        status=GelombangPPDB.DIBUKA,
    )
    data.update(kwargs)
    return GelombangPPDB.objects.create(**data)


class PPDBTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        data_dasar()
        cls.tu = buat_user('tu_ppdb', 'tata_usaha')

    def test_gelombang_luar_tanggal_tidak_efektif(self):
        now = timezone.now()
        g = _gelombang(mulai=now - timedelta(days=10), selesai=now - timedelta(days=1), status=GelombangPPDB.DIBUKA)
        self.assertIsNone(gelombang_terbuka())
        g.refresh_from_db()
        self.assertEqual(g.status, GelombangPPDB.DITUTUP)

    def test_form_tutup_menolak_post(self):
        r = self.client.get(reverse('pendaftaran'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Pendaftaran ditutup')
        r2 = self.client.post(reverse('pendaftaran'), _ppdb_payload())
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(Pendaftaran.objects.count(), 0)

    def test_form_buka_dan_cek_status(self):
        _gelombang()
        r = self.client.post(reverse('pendaftaran'), _ppdb_payload())
        self.assertRedirects(r, reverse('pendaftaran_sukses'))
        p = Pendaftaran.objects.get()
        self.assertTrue(p.kode_pendaftaran)
        cek = self.client.post(reverse('ppdb:cek_status'), {
            'kode': p.kode_pendaftaran,
            'tanggal_lahir': '2010-01-01',
        })
        self.assertContains(cek, p.nama_lengkap)
        self.assertContains(cek, 'Dikirim')
        self.assertNotContains(cek, p.nik)

    def test_jadikan_santri_menyimpan_pendaftaran(self):
        _gelombang()
        self.client.post(reverse('pendaftaran'), _ppdb_payload())
        p = Pendaftaran.objects.get()
        p.status = 'diterima'
        p.save()
        santri = terima_menjadi_santri(p)
        self.assertTrue(Santri.objects.filter(pk=santri.pk).exists())
        self.assertTrue(santri.nomor_induk_santri)
        self.assertEqual(Pendaftaran.objects.filter(pk=p.pk).count(), 1)
        lagi = terima_menjadi_santri(p)
        self.assertEqual(lagi.pk, santri.pk)

    def test_halaman_publik_tanpa_nik_tersimpan(self):
        _gelombang()
        self.client.post(reverse('pendaftaran'), _ppdb_payload())
        nik = Pendaftaran.objects.get().nik
        home = self.client.get(reverse('home'))
        self.assertNotContains(home, nik)
        status = self.client.get(reverse('ppdb:cek_status'))
        self.assertNotContains(status, nik)
