from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from lembaga.factories import buat_santri, buat_user, data_dasar
from keuangan.models import JenisTagihan, Tagihan
from keuangan.services import generate_tagihan_massal, terima_bayar
from akademik.models import KeanggotaanRB


class KeuanganTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = data_dasar()
        cls.bendahara = buat_user('ben_keu', 'bendahara')
        cls.ustadz = buat_user('ust_keu', 'ustadz')
        cls.s1 = buat_santri('NISKEU1', 'Santri Bayar', '3601010101010061')
        cls.s2 = buat_santri('NISKEU2', 'Santri Tunggak', '3601010101010062')
        cls.jenis = JenisTagihan.objects.create(nama='Syahriyah')
        KeanggotaanRB.objects.create(rb=cls.data['rb'], santri=cls.s1)

    def test_generate_massal_tidak_dobel(self):
        dibuat = generate_tagihan_massal(
            self.jenis, Decimal('100000'), date.today() + timedelta(days=7),
            periode=self.data['periode'],
        )
        self.assertEqual(len(dibuat), 2)
        lagi = generate_tagihan_massal(
            self.jenis, Decimal('100000'), date.today() + timedelta(days=7),
            periode=self.data['periode'],
        )
        self.assertEqual(len(lagi), 0)
        rb_only = generate_tagihan_massal(
            JenisTagihan.objects.create(nama='Daftar ulang'),
            Decimal('50000'), date.today(), rb=self.data['rb'],
        )
        self.assertEqual(len(rb_only), 1)

    def test_tolak_bayar_lebih(self):
        tagihan = Tagihan.objects.create(
            santri=self.s1, jenis=self.jenis, periode=self.data['periode'],
            jumlah=Decimal('100000'), jatuh_tempo=date.today(),
        )
        terima_bayar(tagihan, Decimal('40000'), self.bendahara)
        tagihan.refresh_from_db()
        self.assertEqual(tagihan.status, 'sebagian')
        with self.assertRaises(ValidationError):
            terima_bayar(tagihan, Decimal('70000'), self.bendahara)
        lunas = terima_bayar(tagihan, Decimal('60000'), self.bendahara)
        self.assertTrue(lunas.nomor_kwitansi)
        tagihan.refresh_from_db()
        self.assertEqual(tagihan.status, 'lunas')

    def test_menu_hilang_dari_ustadz(self):
        self.client.login(username='ust_keu', password='sandi123')
        r = self.client.get(reverse('keuangan:tagihan'))
        self.assertEqual(r.status_code, 403)
        self.client.logout()
        self.client.login(username='ben_keu', password='sandi123')
        r2 = self.client.get(reverse('keuangan:tagihan'))
        self.assertEqual(r2.status_code, 200)
