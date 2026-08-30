from datetime import date

from django.test import TestCase

from lembaga.factories import buat_santri, data_dasar
from tahfidz.models import ProgressHafalan, SetoranHafalan


class TahfidzTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        data_dasar()
        cls.santri = buat_santri('NISTHF', 'Hafidz Uji', '3601010101010077')

    def test_tasmi_menandai_juz_selesai(self):
        SetoranHafalan.objects.create(
            santri=self.santri, jenis=SetoranHafalan.TASMI,
            dari_juz=1, dari_halaman=1, sampai_juz=1, sampai_halaman=20,
            mutu='lancar', tanggal=date.today(),
        )
        progress = ProgressHafalan.objects.get(santri=self.santri)
        self.assertEqual(progress.juz_selesai, 1)

    def test_mutu_kurang_tidak_menambah(self):
        SetoranHafalan.objects.create(
            santri=self.santri, jenis=SetoranHafalan.ZIYADAH,
            dari_juz=1, dari_halaman=1, sampai_juz=1, sampai_halaman=10,
            mutu='kurang', tanggal=date.today(),
        )
        progress = ProgressHafalan.objects.get(santri=self.santri)
        self.assertEqual(progress.juz_selesai, 0)
        self.assertEqual(progress.halaman_berjalan, 1)

    def test_ziyadah_menambah_halaman(self):
        SetoranHafalan.objects.create(
            santri=self.santri, jenis=SetoranHafalan.ZIYADAH,
            dari_juz=1, dari_halaman=1, sampai_juz=1, sampai_halaman=5,
            mutu='lancar', tanggal=date.today(),
        )
        progress = ProgressHafalan.objects.get(santri=self.santri)
        self.assertEqual(progress.halaman_berjalan, 5)

    def test_murojaah_tidak_tambah_juz(self):
        SetoranHafalan.objects.create(
            santri=self.santri, jenis=SetoranHafalan.TASMI,
            dari_juz=1, dari_halaman=1, sampai_juz=2, sampai_halaman=20,
            mutu='cukup', tanggal=date.today(),
        )
        progress = ProgressHafalan.objects.get(santri=self.santri)
        selesai = progress.juz_selesai
        SetoranHafalan.objects.create(
            santri=self.santri, jenis=SetoranHafalan.MUROJAAH,
            dari_juz=1, dari_halaman=1, sampai_juz=2, sampai_halaman=20,
            mutu='lancar', tanggal=date.today(),
        )
        progress.refresh_from_db()
        self.assertEqual(progress.juz_selesai, selesai)
