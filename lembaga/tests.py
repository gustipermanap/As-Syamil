from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from lembaga.factories import buat_user, data_dasar
from lembaga.models import Pengaturan, TahunAjaran, UnitPendidikan, Jenjang
from pengguna.context_processors import menu_flags


class LembagaTests(TestCase):
    def test_pengelola_keuangan_menggeser_menu(self):
        data_dasar()
        tu = buat_user('tu1', 'tata_usaha')
        bendahara = buat_user('ben1', 'bendahara')
        p = Pengaturan.get()
        p.pengelola_keuangan = Pengaturan.PENGELOLA_BENDAHARA
        p.save()
        self.assertTrue(menu_flags(bendahara)['boleh_keuangan'])
        self.assertFalse(menu_flags(tu)['boleh_keuangan'])
        p.pengelola_keuangan = Pengaturan.PENGELOLA_TU
        p.save()
        self.assertTrue(menu_flags(tu)['boleh_keuangan'])
        self.assertFalse(menu_flags(bendahara)['boleh_keuangan'])

    def test_unit_tahfidz_mati_sembunyikan_setoran(self):
        data = data_dasar()
        data['tahfidz'].aktif = False
        data['tahfidz'].save()
        p = Pengaturan.get()
        self.assertFalse(menu_flags()['tahfidz'])
        p.modul_tahfidz = False
        p.save()
        data['tahfidz'].aktif = True
        data['tahfidz'].save()
        self.assertFalse(menu_flags()['tahfidz'])

    def test_jenjang_nama_bebas_dan_satu_tahun_aktif(self):
        data_dasar()
        unit = UnitPendidikan.objects.get(nama='Diniyah Uji')
        j = Jenjang.objects.create(unit=unit, nama='Nama Bebas 99', urutan=9)
        self.assertEqual(j.nama, 'Nama Bebas 99')
        ta2 = TahunAjaran.objects.create(
            nama='lain', mulai=date.today(), selesai=date.today() + timedelta(days=10), aktif=True,
        )
        self.assertTrue(ta2.aktif)
        self.assertEqual(TahunAjaran.objects.filter(aktif=True).count(), 1)

    def test_halaman_pengaturan_tu(self):
        data_dasar()
        buat_user('tu2', 'tata_usaha')
        self.client.login(username='tu2', password='sandi123')
        r = self.client.get(reverse('lembaga:pengaturan'))
        self.assertEqual(r.status_code, 200)
        self.client.post(reverse('lembaga:pengaturan'), {
            'nama_tampil': 'Pesantren Uji',
            'pengelola_keuangan': 'tata_usaha',
            'jenis_periode': 'semester',
            'predikat_a': 90, 'predikat_b': 80, 'predikat_c': 70, 'predikat_d': 60,
            'ambang_alpa': 3,
            'modul_ppdb': 'on', 'modul_akademik': 'on', 'modul_tahfidz': 'on',
            'modul_asrama': 'on', 'modul_keuangan': 'on', 'modul_kedisiplinan': 'on',
        })
        self.assertEqual(Pengaturan.get().pengelola_keuangan, 'tata_usaha')
        self.assertEqual(Pengaturan.get().nama_tampil, 'Pesantren Uji')
