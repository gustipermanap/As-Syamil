from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from kesiswaan.models import (
    CatatanPelanggaran, Gedung, Izin, JenisPelanggaran, Kamar,
    Pegawai, PenempatanKamar, Santri, WaliSantri,
)
from kesiswaan.services import proses_izin
from lembaga.factories import buat_santri, buat_user, data_dasar
from akademik.models import KeanggotaanRB


class KesiswaanTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = data_dasar()
        cls.tu = buat_user('tu_kes', 'tata_usaha')
        cls.wali1 = buat_user('wali_a', 'wali')
        cls.wali2 = buat_user('wali_b', 'wali')
        cls.w1 = WaliSantri.objects.create(nama='Wali A', user=cls.wali1)
        cls.w2 = WaliSantri.objects.create(nama='Wali B', user=cls.wali2)
        cls.s1 = buat_santri('NIS001', 'Santri A', '3601010101010001', wali=cls.w1)
        cls.s2 = buat_santri('NIS002', 'Santri B', '3601010101010002', wali=cls.w2, jk='P')

    def test_nis_unik(self):
        with self.assertRaises(Exception):
            buat_santri('NIS001', 'Duplikat', '3601010101010099')

    def test_nik_dobel_aktif_ditolak(self):
        with self.assertRaises(ValidationError):
            buat_santri('NIS003', 'Kembar NIK', '3601010101010001')

    def test_banyak_rb(self):
        KeanggotaanRB.objects.create(rb=self.data['rb'], santri=self.s1)
        from akademik.models import RuangBelajar, RombonganBelajar
        ruang2 = RuangBelajar.objects.create(
            unit=self.data['unit'], nama='Halaqah 2', tipe='halaqah',
        )
        rb2 = RombonganBelajar.objects.create(
            ruang=ruang2, tahun_ajaran=self.data['ta'], nama='RB 2',
        )
        KeanggotaanRB.objects.create(rb=rb2, santri=self.s1)
        self.assertEqual(self.s1.keanggotaan_rb.count(), 2)

    def test_pegawai_nonaktif_gagal_masuk(self):
        user = buat_user('peg_off', 'ustadz')
        Pegawai.objects.create(nama='Ustadz Off', jenis_kelamin='L', user=user, aktif=True)
        peg = Pegawai.objects.get(nama='Ustadz Off')
        peg.aktif = False
        peg.save()
        ok = self.client.login(username='peg_off', password='sandi123')
        self.assertFalse(ok)

    def test_kamar_jenis_kelamin_dan_kapasitas(self):
        gedung = Gedung.objects.create(nama='Putra', putra_putri='L')
        kamar = Kamar.objects.create(gedung=gedung, nama='K1', kapasitas=1)
        PenempatanKamar.objects.create(santri=self.s1, kamar=kamar, masuk=date.today())
        with self.assertRaises(ValidationError):
            PenempatanKamar(santri=self.s2, kamar=kamar, masuk=date.today()).full_clean()
        s3 = buat_santri('NIS004', 'Santri C', '3601010101010003')
        with self.assertRaises(ValidationError):
            PenempatanKamar(santri=s3, kamar=kamar, masuk=date.today()).full_clean()

    def test_izin_alur(self):
        now = timezone.now()
        izin = Izin.objects.create(
            santri=self.s1, jenis='pulang', status='diajukan',
            mulai=now, selesai=now + timedelta(days=1),
        )
        proses_izin(izin, 'setujui')
        self.assertEqual(izin.status, 'disetujui')
        proses_izin(izin, 'mulai')
        self.assertEqual(izin.status, 'berlangsung')
        proses_izin(izin, 'kembali', saat=now)
        self.assertEqual(izin.status, 'selesai')
        izin2 = Izin.objects.create(
            santri=self.s1, jenis='pulang', status='diajukan',
            mulai=now - timedelta(days=3), selesai=now - timedelta(days=1),
        )
        proses_izin(izin2, 'setujui')
        proses_izin(izin2, 'mulai')
        proses_izin(izin2, 'kembali', saat=now)
        self.assertEqual(izin2.status, 'terlambat')

    def test_poin_pelanggaran(self):
        jenis = JenisPelanggaran.objects.create(nama='Ramai', poin=3)
        CatatanPelanggaran.objects.create(santri=self.s1, jenis=jenis, tanggal=date.today())
        CatatanPelanggaran.objects.create(santri=self.s1, jenis=jenis, tanggal=date.today())
        poin = sum(p.jenis.poin for p in self.s1.pelanggaran.all())
        self.assertEqual(poin, 6)

    def test_wali_hanya_anaknya(self):
        self.client.login(username='wali_a', password='sandi123')
        r = self.client.get(reverse('pengguna:wali'))
        self.assertContains(r, 'Santri A')
        self.assertNotContains(r, 'Santri B')
        r2 = self.client.get(reverse('pengguna:rapor', args=[self.s2.pk]))
        self.assertEqual(r2.status_code, 403)

    def test_halaman_santri_operasi(self):
        self.client.login(username='tu_kes', password='sandi123')
        r = self.client.get(reverse('kesiswaan:santri'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Santri A')
        d = self.client.get(reverse('kesiswaan:santri_detail', args=[self.s1.pk]))
        self.assertEqual(d.status_code, 200)
        self.assertContains(d, 'Santri A')
