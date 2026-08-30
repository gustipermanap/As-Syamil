from datetime import date, time
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from akademik.models import (
    Absensi, JadwalSlot, KeanggotaanRB, KitabAtauMapel, Penilaian,
    PengampuRB, Pertemuan, RombonganBelajar, RuangBelajar,
)
from kesiswaan.models import Pegawai
from lembaga.factories import buat_santri, buat_user, data_dasar
from lembaga.models import Pengaturan, UnitPendidikan


class AkademikTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = data_dasar()
        cls.tu = buat_user('tu_akd', 'tata_usaha')
        cls.ustadz_user = buat_user('ustadz_akd', 'ustadz')
        cls.ustadz_lain = buat_user('ustadz_lain', 'ustadz')
        cls.peg = Pegawai.objects.create(nama='Pengampu Uji', jenis_kelamin='L', user=cls.ustadz_user)
        Pegawai.objects.create(nama='Lain', jenis_kelamin='L', user=cls.ustadz_lain)
        PengampuRB.objects.create(rb=cls.data['rb'], pegawai=cls.peg)
        cls.mapel = KitabAtauMapel.objects.create(
            unit=cls.data['unit'], nama='Jurumiyah', jenis='kitab',
        )
        cls.mapel_formal = KitabAtauMapel.objects.create(
            unit=UnitPendidikan.objects.create(nama='MTs Uji', tipe='formal'),
            nama='Matematika', jenis='mapel_umum',
        )
        cls.santri = buat_santri('NISAK1', 'Santri Nilai', '3601010101010088')
        KeanggotaanRB.objects.create(rb=cls.data['rb'], santri=cls.santri)
        cls.slot = JadwalSlot.objects.create(
            rb=cls.data['rb'], hari=0, jam_mulai=time(7, 0), jam_selesai=time(8, 0),
            mapel=cls.mapel, pengampu=cls.peg,
        )

    def test_mapel_beda_unit(self):
        self.assertNotEqual(self.mapel.unit_id, self.mapel_formal.unit_id)
        self.assertEqual(self.mapel.jenis, 'kitab')
        self.assertEqual(self.mapel_formal.jenis, 'mapel_umum')

    def test_ustadz_hanya_jadwal_ampuan(self):
        self.client.login(username='ustadz_akd', password='sandi123')
        r = self.client.get(reverse('akademik:jadwal'))
        self.assertContains(r, 'Jurumiyah')
        self.client.logout()
        self.client.login(username='ustadz_lain', password='sandi123')
        r2 = self.client.get(reverse('akademik:jadwal'))
        self.assertNotContains(r2, 'Jurumiyah')

    def test_absensi_empat_status(self):
        pertemuan = Pertemuan.objects.create(
            rb=self.data['rb'], mapel=self.mapel, pengampu=self.peg, tanggal=date.today(),
        )
        self.client.login(username='ustadz_akd', password='sandi123')
        r = self.client.post(reverse('akademik:isi_absensi', args=[pertemuan.pk]), {
            f'status_{self.santri.pk}': 'alpa',
        })
        self.assertEqual(r.status_code, 302)
        absen = Absensi.objects.get(pertemuan=pertemuan, santri=self.santri)
        self.assertEqual(absen.status, 'alpa')
        for st in ('hadir', 'izin', 'sakit', 'alpa'):
            Absensi.objects.filter(pk=absen.pk).update(status=st)
            absen.refresh_from_db()
            self.assertEqual(absen.status, st)

    def test_predikat_dari_pengaturan(self):
        p = Pengaturan.get()
        self.assertEqual(p.predikat(95), 'A')
        self.assertEqual(p.predikat(85), 'B')
        self.assertEqual(p.predikat(75), 'C')
        self.assertEqual(p.predikat(65), 'D')
        self.assertEqual(p.predikat(50), 'E')
        nilai = Penilaian.objects.create(
            santri=self.santri, mapel=self.mapel, rb=self.data['rb'],
            periode=self.data['periode'], jenis='akhir', nilai=Decimal('91'),
        )
        self.assertEqual(nilai.predikat, 'A')
        p.predikat_a = 95
        p.save()
        nilai.nilai = Decimal('91')
        nilai.save()
        self.assertEqual(nilai.predikat, 'B')

    def test_rapor_tu_dan_wali(self):
        Penilaian.objects.create(
            santri=self.santri, mapel=self.mapel, rb=self.data['rb'],
            periode=self.data['periode'], jenis='akhir', nilai=Decimal('80'),
        )
        self.client.login(username='tu_akd', password='sandi123')
        r = self.client.get(reverse('pengguna:rapor', args=[self.santri.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Jurumiyah')
