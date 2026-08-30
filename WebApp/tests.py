from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from django.utils import timezone
from datetime import timedelta

from ppdb.models import GelombangPPDB
from .models import DataSekolah, Pendaftaran, Post, message


def _ppdb_payload(**overrides):
    data = {
        'nama_lengkap': 'Ahmad Fulan',
        'nik': '1234567890123456',
        'jenis_kelamin': 'L',
        'nisn': '123456789012',
        'tempat_lahir': 'Pandeglang',
        'tanggal_lahir': '2010-01-01',
        'agama': 'Islam',
        'no_handphone': '08123456789',
        'anak_ke': 1,
        'jumlah_saudara': 2,
        'asal_sekolah': 'SMP',
        'tgl_no_ijazah': '2024-06-01',
        'lama_belajar': 3,
        'rt': '01',
        'rw': '02',
        'kelurahan': 'Kaungcaang',
        'kecamatan': 'Cadasari',
        'kota_kabupaten': 'Pandeglang',
        'kode_pos': '42251',
        'nama_ayah': 'Bapak Fulan',
        'nama_ibu': 'Ibu Fulan',
        'pekerjaan_ayah': 'Tani',
        'pekerjaan_ibu': 'IRT',
        'pendidikan_ayah': 'SMA',
        'pendidikan_ibu': 'SMA',
        'penghasilan_bulanan': '1000000',
        'ktp_ayah': True,
        'ktp_ibu': True,
        'alamat_orangtua': 'Kp. Parasi',
        'alamat': 'Kp. Parasi',
    }
    data.update(overrides)
    return data


class WebsiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        DataSekolah.objects.create(
            nama_sekolah='Pondok Pesantren As-Syamil',
            alamat='Kp. Parasi, Cadasari, Pandeglang',
            email='ponpesassyamil@gmail.com',
            contact='6282128333839',
            whatsapp='6282128333839',
            ppdb_periode='1 Mei 2026 - 30 Juni 2026',
            open_hours='Senin-Sabtu: 07.00 - 16.00',
        )
        now = timezone.now()
        GelombangPPDB.objects.create(
            nama='Gelombang uji',
            mulai=now - timedelta(days=1),
            selesai=now + timedelta(days=30),
            kuota=100,
            status=GelombangPPDB.DIBUKA,
        )
        author = User.objects.create_user(username='admincms', password='pass')
        Post.objects.create(
            title='Kegiatan Pondok',
            slug='kegiatan-pondok',
            content='Santri mengikuti kegiatan rutin.',
            author=author,
        )

    def test_beranda_ok(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'As-Syamil')
        self.assertContains(response, 'Kegiatan Pondok')
        self.assertContains(response, reverse('pengguna:masuk'))

    def test_login_bukan_beranda(self):
        self.assertNotEqual(reverse('pengguna:masuk'), reverse('home'))
        response = self.client.get(reverse('admin:index'), follow=False)
        self.assertIn(response.status_code, (200, 302))
        if response.status_code == 302:
            self.assertIn('/admin/login', response['Location'])

    def test_kontak_menampilkan_data_sekolah(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ponpesassyamil@gmail.com')
        self.assertContains(response, '6282128333839')

    def test_kontak_menyimpan_pesan(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Tamu',
            'email': 'tamu@example.com',
            'subject': 'Tanya PPDB',
            'message': 'Apakah masih buka pendaftaran?',
        })
        self.assertRedirects(response, reverse('success'))
        self.assertEqual(message.objects.count(), 1)
        self.assertEqual(message.objects.get().subject, 'Tanya PPDB')

    def test_halaman_sukses_kontak(self):
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pesan terkirim')

    def test_ppdb_get(self):
        response = self.client.get(reverse('pendaftaran'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, 'Gelombang uji')

    def test_ppdb_menyimpan_dan_redirect_sukses(self):
        response = self.client.post(reverse('pendaftaran'), _ppdb_payload())
        self.assertRedirects(response, reverse('pendaftaran_sukses'))
        self.assertEqual(Pendaftaran.objects.count(), 1)
        obj = Pendaftaran.objects.get()
        self.assertEqual(obj.nama_lengkap, 'Ahmad Fulan')
        self.assertTrue(obj.kode_pendaftaran)
        self.assertEqual(obj.status, 'dikirim')

    def test_ppdb_sukses_halaman(self):
        response = self.client.get(reverse('pendaftaran_sukses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pendaftaran terkirim')

    def test_blog_list_dan_detail(self):
        listing = self.client.get(reverse('post_list'))
        self.assertEqual(listing.status_code, 200)
        self.assertContains(listing, 'Kegiatan Pondok')

        detail = self.client.get(reverse('blog_detail', args=['kegiatan-pondok']))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, 'Santri mengikuti kegiatan rutin.')

    def test_whatsapp_url(self):
        sekolah = DataSekolah.objects.first()
        self.assertEqual(sekolah.whatsapp_url, 'https://wa.me/6282128333839')
