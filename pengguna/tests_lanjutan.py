from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from akademik.models import KitabAtauMapel, Penilaian
from kesiswaan.models import Izin, Pegawai, WaliSantri
from kesiswaan.services import proses_izin
from keuangan.models import JenisTagihan, Tagihan
from lembaga.factories import buat_santri, buat_user, data_dasar
from pengguna.models import LogAkses, Notifikasi
from ppdb.models import GelombangPPDB
from WebApp.models import Pendaftaran
from WebApp.tests import _ppdb_payload


def _jpeg(nama='foto.jpg'):
    buf = BytesIO()
    Image.new('RGB', (12, 12), color='red').save(buf, format='JPEG')
    return SimpleUploadedFile(nama, buf.getvalue(), content_type='image/jpeg')


class CrudUbahTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = data_dasar()
        cls.tu = buat_user('tu_crud', 'tata_usaha')
        cls.santri = buat_santri('NISCRUD', 'Santri CRUD', '3601010101010400')

    def setUp(self):
        self.client.login(username='tu_crud', password='sandi123')

    def test_ubah_unit(self):
        unit = self.data['unit']
        r = self.client.post(reverse('lembaga:unit_ubah', args=[unit.pk]), {
            'nama': 'Diniyah Diubah',
            'tipe': unit.tipe,
            'aktif': 'on',
            'label_peserta': 'Santri',
        })
        self.assertEqual(r.status_code, 302)
        unit.refresh_from_db()
        self.assertEqual(unit.nama, 'Diniyah Diubah')

    def test_taut_akun_pegawai(self):
        peg = Pegawai.objects.create(nama='Ustadz Baru', jenis_kelamin='L', aktif=True)
        r = self.client.post(reverse('kesiswaan:pegawai_ubah', args=[peg.pk]), {
            'nama': 'Ustadz Baru',
            'jenis_kelamin': 'L',
            'aktif': 'on',
            'username': 'ustadz_baru',
            'sandi': 'sandi123',
            'grup': 'ustadz',
        })
        self.assertEqual(r.status_code, 302)
        peg.refresh_from_db()
        self.assertIsNotNone(peg.user_id)
        self.assertTrue(self.client.login(username='ustadz_baru', password='sandi123'))

    def test_taut_akun_santri(self):
        r = self.client.post(reverse('kesiswaan:santri_ubah', args=[self.santri.pk]), {
            'nomor_induk_santri': self.santri.nomor_induk_santri,
            'nisn': self.santri.nisn,
            'nama': self.santri.nama,
            'nik': self.santri.nik,
            'tanggal_lahir': '2012-01-01',
            'jenis_kelamin': 'L',
            'status': 'aktif',
            'username': 'santri_crud',
            'sandi': 'sandi123',
        })
        self.assertEqual(r.status_code, 302)
        self.santri.refresh_from_db()
        self.assertIsNotNone(self.santri.user_id)
        self.assertTrue(self.client.login(username='santri_crud', password='sandi123'))


class PortalSantriLanjutanTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = data_dasar()
        cls.user = buat_user('santri_lanjut', 'santri')
        cls.santri = buat_santri('NISLAN', 'Santri Portal Lanjut', '3601010101010500')
        cls.santri.user = cls.user
        cls.santri.save()
        cls.mapel = KitabAtauMapel.objects.create(
            unit=cls.data['unit'], nama='Imrithi', jenis='kitab',
        )
        Penilaian.objects.create(
            santri=cls.santri, mapel=cls.mapel, rb=cls.data['rb'],
            periode=cls.data['periode'], jenis='akhir', nilai=Decimal('87'),
        )
        cls.jenis = JenisTagihan.objects.create(nama='Syahriyah portal')
        Tagihan.objects.create(
            santri=cls.santri, jenis=cls.jenis, periode=cls.data['periode'],
            jumlah=Decimal('150000'), jatuh_tempo=date.today() + timedelta(days=5),
        )

    def test_portal_menampilkan_nilai_dan_tagihan(self):
        self.client.login(username='santri_lanjut', password='sandi123')
        r = self.client.get(reverse('pengguna:santri'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Imrithi')
        self.assertContains(r, '87')
        self.assertContains(r, 'Syahriyah portal')
        self.assertContains(r, '150000')

    def test_santri_unduh_rapor_pdf_dan_log_akses(self):
        self.client.login(username='santri_lanjut', password='sandi123')
        r = self.client.get(reverse('pengguna:rapor', args=[self.santri.pk]), {'format': 'pdf'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'application/pdf')
        self.assertTrue(r.content.startswith(b'%PDF'))
        self.assertTrue(LogAkses.objects.filter(
            user=self.user, aksi='lihat_rapor', objek='NISLAN',
        ).exists())


class NotifikasiPrivasiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        data_dasar()
        cls.tu = buat_user('tu_notif', 'tata_usaha')
        cls.pemohon = buat_user('wali_notif', 'wali')
        cls.wali = WaliSantri.objects.create(nama='Wali Notif', user=cls.pemohon)
        cls.santri = buat_santri('NISNTF', 'Santri Notif', '3601010101010600', wali=cls.wali)

    def test_izin_setujui_mengirim_notifikasi(self):
        now = timezone.now()
        izin = Izin.objects.create(
            santri=self.santri, jenis='pulang', status='diajukan',
            mulai=now, selesai=now + timedelta(days=1),
            pemohon=self.pemohon,
        )
        proses_izin(izin, 'setujui')
        notif = Notifikasi.objects.get(penerima=self.pemohon)
        self.assertIn('Disetujui', notif.judul)
        self.assertEqual(notif.tautan, '/wali/')

    def test_halaman_privasi(self):
        r = self.client.get(reverse('pengguna:privasi'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Kebijakan privasi')
        self.assertNotContains(r, '3601010101010600')


class PotonganTagihanTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = data_dasar()
        cls.bendahara = buat_user('ben_potong', 'bendahara')
        cls.santri = buat_santri('NISPOT', 'Santri Potongan', '3601010101010700')
        cls.jenis = JenisTagihan.objects.create(nama='Syahriyah potong')
        cls.tagihan = Tagihan.objects.create(
            santri=cls.santri, jenis=cls.jenis, periode=cls.data['periode'],
            jumlah=Decimal('100000'), jatuh_tempo=date.today(),
        )

    def test_potongan_mengurangi_sisa_dan_bisa_lunaskan(self):
        self.assertEqual(self.tagihan.sisa(), Decimal('100000'))
        self.client.login(username='ben_potong', password='sandi123')
        r = self.client.post(reverse('keuangan:tagihan_potongan', args=[self.tagihan.pk]), {
            'potongan': '40000',
        })
        self.assertEqual(r.status_code, 302)
        self.tagihan.refresh_from_db()
        self.assertEqual(self.tagihan.potongan, Decimal('40000'))
        self.assertEqual(self.tagihan.sisa(), Decimal('60000'))
        r2 = self.client.post(reverse('keuangan:tagihan_potongan', args=[self.tagihan.pk]), {
            'potongan': '150000',
        })
        self.assertEqual(r2.status_code, 200)
        self.tagihan.refresh_from_db()
        self.assertEqual(self.tagihan.potongan, Decimal('40000'))


class BerkasPPDBTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        data_dasar()
        now = timezone.now()
        GelombangPPDB.objects.create(
            nama='Berkas ulang',
            mulai=now - timedelta(days=1),
            selesai=now + timedelta(days=10),
            kuota=10,
            status=GelombangPPDB.DIBUKA,
        )

    def test_unggah_ulang_foto_jika_berkas_kurang(self):
        self.client.post(reverse('pendaftaran'), _ppdb_payload(nama_lengkap='Calon Berkas'))
        p = Pendaftaran.objects.get(nama_lengkap='Calon Berkas')
        p.status = 'berkas_kurang'
        p.save()
        r = self.client.post(reverse('ppdb:cek_status'), {
            'kode': p.kode_pendaftaran,
            'tanggal_lahir': '2010-01-01',
            'foto': _jpeg(),
        })
        self.assertEqual(r.status_code, 200)
        p.refresh_from_db()
        self.assertEqual(p.status, 'dikirim')
        self.assertTrue(p.foto)
        self.assertContains(r, 'Dikirim')
