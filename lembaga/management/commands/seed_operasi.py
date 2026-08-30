from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.utils import timezone

from akademik.models import (
    Absensi, JadwalSlot, KeanggotaanRB, KitabAtauMapel, MapelRB,
    Penilaian, PengampuRB, Pertemuan, RombonganBelajar, RuangBelajar,
)
from kesiswaan.models import (
    CatatanPelanggaran, Gedung, Izin, JenisPelanggaran, Kamar,
    Pegawai, PenempatanKamar, Santri, WaliSantri,
)
from keuangan.models import JenisTagihan, Tagihan
from keuangan.services import terima_bayar
from lembaga.models import Jenjang, Pengaturan, Periode, TahunAjaran, UnitPendidikan
from pengguna.services import pastikan_grup
from ppdb.models import GelombangPPDB
from tahfidz.models import SetoranHafalan
from WebApp.models import DataSekolah, Pendaftaran


SANDI = 'sandi123'


def _user(username, grup, **kwargs):
    user, created = User.objects.get_or_create(username=username, defaults=kwargs)
    if created:
        user.set_password(SANDI)
        user.save()
    g, _ = Group.objects.get_or_create(name=grup)
    user.groups.add(g)
    return user


class Command(BaseCommand):
    help = 'Mengisi data contoh agar sistem bisa dioperasikan.'

    def handle(self, *args, **options):
        pastikan_grup()
        pengaturan = Pengaturan.get()
        pengaturan.nama_tampil = 'Pondok Pesantren As-Syamil'
        pengaturan.pengelola_keuangan = Pengaturan.PENGELOLA_BENDAHARA
        pengaturan.portal_santri_aktif = True
        pengaturan.modul_ppdb = True
        pengaturan.modul_akademik = True
        pengaturan.modul_tahfidz = True
        pengaturan.modul_asrama = True
        pengaturan.modul_keuangan = True
        pengaturan.save()

        if not DataSekolah.objects.exists():
            DataSekolah.objects.create(
                nama_sekolah='Pondok Pesantren As-Syamil',
                alamat='Kp. Parasi, Cadasari, Pandeglang',
                email='ponpesassyamil@gmail.com',
                contact='6282128333839',
                whatsapp='6282128333839',
                ppdb_periode='Mengikuti gelombang PPDB',
            )

        diniyah, _ = UnitPendidikan.objects.get_or_create(
            nama='Diniyah', defaults={'tipe': 'diniyah', 'aktif': True},
        )
        tahfidz_unit, _ = UnitPendidikan.objects.get_or_create(
            nama='Tahfidz', defaults={'tipe': 'tahfidz', 'aktif': True},
        )
        UnitPendidikan.objects.get_or_create(
            nama='Asrama Putra-Putri', defaults={'tipe': 'asrama', 'aktif': True},
        )
        wustha, _ = Jenjang.objects.get_or_create(unit=diniyah, nama='Wustha', defaults={'urutan': 2})
        Jenjang.objects.get_or_create(unit=tahfidz_unit, nama='Hifdz', defaults={'urutan': 1})

        hari = date.today()
        ta, _ = TahunAjaran.objects.get_or_create(
            nama='2026/2027',
            defaults={
                'mulai': date(hari.year, 7, 1),
                'selesai': date(hari.year + 1, 6, 30),
                'aktif': True,
            },
        )
        if not ta.aktif:
            ta.aktif = True
            ta.save()
        periode, _ = Periode.objects.get_or_create(
            tahun_ajaran=ta,
            nama='Ganjil',
            defaults={'mulai': ta.mulai, 'selesai': date(ta.mulai.year, 12, 31), 'aktif': True},
        )

        mudir = _user('mudir', 'mudir', first_name='Mudir')
        tu = _user('tu', 'tata_usaha', first_name='Tata Usaha')
        bendahara = _user('bendahara', 'bendahara', first_name='Bendahara')
        ustadz = _user('ustadz1', 'ustadz', first_name='Ustadz Ahmad')
        ustadz2 = _user('ustadz2', 'ustadz', first_name='Ustadzah Fatimah')
        musyrif = _user('musyrif1', 'musyrif', first_name='Musyrif')
        wali1 = _user('wali1', 'wali', first_name='Wali Satu')
        wali2 = _user('wali2', 'wali', first_name='Wali Dua')
        santri_akun = _user('santri1', 'santri', first_name='Santri Portal')

        peg_ustadz, _ = Pegawai.objects.get_or_create(
            nama='Ustadz Ahmad', defaults={'jenis_kelamin': 'L', 'user': ustadz},
        )
        if not peg_ustadz.user_id:
            peg_ustadz.user = ustadz
            peg_ustadz.save()
        Pegawai.objects.get_or_create(nama='Ustadzah Fatimah', defaults={'jenis_kelamin': 'P', 'user': ustadz2})
        Pegawai.objects.get_or_create(nama='Musyrif Hasan', defaults={'jenis_kelamin': 'L', 'user': musyrif})
        Pegawai.objects.get_or_create(nama='Staf TU', defaults={'jenis_kelamin': 'L', 'user': tu})
        Pegawai.objects.get_or_create(nama='Bendahara Pondok', defaults={'jenis_kelamin': 'P', 'user': bendahara})
        Pegawai.objects.get_or_create(nama='Mudir Pondok', defaults={'jenis_kelamin': 'L', 'user': mudir})

        w1, _ = WaliSantri.objects.get_or_create(
            nama='Bapak Abdullah', defaults={'user': wali1, 'kontak': '081111111111'},
        )
        if not w1.user_id:
            w1.user = wali1
            w1.save()
        w2, _ = WaliSantri.objects.get_or_create(
            nama='Ibu Khadijah', defaults={'user': wali2, 'kontak': '082222222222'},
        )
        if not w2.user_id:
            w2.user = wali2
            w2.save()

        data_santri = [
            ('ASY20260001', 'Ahmad Zaki', 'L', '3601010101010001', w1, santri_akun),
            ('ASY20260002', 'Muhammad Iqbal', 'L', '3601010101010002', w1, None),
            ('ASY20260003', 'Hasan Basri', 'L', '3601010101010003', w1, None),
            ('ASY20260004', 'Fatimah Azzahra', 'P', '3601010101010004', w2, None),
            ('ASY20260005', 'Aisyah Putri', 'P', '3601010101010005', w2, None),
        ]
        santri_objs = []
        for nis, nama, jk, nik, wali, akun in data_santri:
            s, created = Santri.objects.get_or_create(
                nomor_induk_santri=nis,
                defaults={
                    'nama': nama,
                    'nik': nik,
                    'jenis_kelamin': jk,
                    'status': 'aktif',
                    'wali': wali,
                    'user': akun,
                    'tempat_lahir': 'Pandeglang',
                    'tanggal_lahir': date(2012, 1, 1),
                    'nisn': '1234567890',
                },
            )
            santri_objs.append(s)

        ruang, _ = RuangBelajar.objects.get_or_create(
            nama='Halaqah Wustha A',
            defaults={'unit': diniyah, 'jenjang': wustha, 'tipe': 'halaqah'},
        )
        rb, _ = RombonganBelajar.objects.get_or_create(
            ruang=ruang, tahun_ajaran=ta, defaults={'nama': 'Halaqah Wustha A 2026/2027'},
        )
        PengampuRB.objects.get_or_create(rb=rb, pegawai=peg_ustadz, defaults={'sebagai_wali': True})
        for s in santri_objs:
            KeanggotaanRB.objects.get_or_create(rb=rb, santri=s)

        kitab, _ = KitabAtauMapel.objects.get_or_create(
            nama='Jurumiyah', defaults={'unit': diniyah, 'jenjang': wustha, 'jenis': 'kitab'},
        )
        MapelRB.objects.get_or_create(rb=rb, mapel=kitab)
        JadwalSlot.objects.get_or_create(
            rb=rb, hari=0, jam_mulai='07:00', jam_selesai='08:30',
            defaults={'mapel': kitab, 'pengampu': peg_ustadz},
        )
        pertemuan, _ = Pertemuan.objects.get_or_create(
            rb=rb, mapel=kitab, tanggal=hari,
            defaults={'pengampu': peg_ustadz, 'catatan': 'Pertemuan contoh'},
        )
        Absensi.objects.get_or_create(
            pertemuan=pertemuan, santri=santri_objs[0], defaults={'status': 'hadir'},
        )
        Absensi.objects.get_or_create(
            pertemuan=pertemuan, santri=santri_objs[1], defaults={'status': 'alpa'},
        )
        Penilaian.objects.get_or_create(
            santri=santri_objs[0], mapel=kitab, rb=rb, periode=periode, jenis='akhir',
            defaults={'nilai': Decimal('88')},
        )

        gedung_l, _ = Gedung.objects.get_or_create(nama='Asrama Putra', defaults={'putra_putri': 'L'})
        gedung_p, _ = Gedung.objects.get_or_create(nama='Asrama Putri', defaults={'putra_putri': 'P'})
        kamar_l, _ = Kamar.objects.get_or_create(gedung=gedung_l, nama='Kamar 1', defaults={'kapasitas': 8})
        kamar_p, _ = Kamar.objects.get_or_create(gedung=gedung_p, nama='Kamar A', defaults={'kapasitas': 8})
        PenempatanKamar.objects.get_or_create(
            santri=santri_objs[0], kamar=kamar_l, keluar=None, defaults={'masuk': hari},
        )
        PenempatanKamar.objects.get_or_create(
            santri=santri_objs[3], kamar=kamar_p, keluar=None, defaults={'masuk': hari},
        )

        now = timezone.now()
        GelombangPPDB.objects.get_or_create(
            nama='Gelombang 1 1447 H',
            defaults={
                'mulai': now - timedelta(days=7),
                'selesai': now + timedelta(days=30),
                'kuota': 80,
                'status': GelombangPPDB.DIBUKA,
                'unit_tujuan': diniyah,
            },
        )
        Pendaftaran.objects.get_or_create(
            kode_pendaftaran='CONTOH01',
            defaults={
                'nama_lengkap': 'Calon Contoh',
                'nik': '3601010101010099',
                'jenis_kelamin': 'L',
                'nisn': '109876543210',
                'tempat_lahir': 'Pandeglang',
                'tanggal_lahir': date(2011, 5, 5),
                'agama': 'Islam',
                'no_handphone': '083333333333',
                'anak_ke': 1,
                'jumlah_saudara': 1,
                'asal_sekolah': 'MTs',
                'tgl_no_ijazah': date(2024, 6, 1),
                'lama_belajar': 3,
                'rt': '01',
                'rw': '02',
                'kelurahan': 'Kaungcaang',
                'kecamatan': 'Cadasari',
                'kota_kabupaten': 'Pandeglang',
                'kode_pos': '42251',
                'nama_ayah': 'Ayah Contoh',
                'nama_ibu': 'Ibu Contoh',
                'pekerjaan_ayah': 'Tani',
                'pekerjaan_ibu': 'IRT',
                'pendidikan_ayah': 'SMA',
                'pendidikan_ibu': 'SMA',
                'penghasilan_bulanan': Decimal('1000000'),
                'ktp_ayah': True,
                'ktp_ibu': True,
                'alamat_orangtua': 'Kp. Parasi',
                'alamat': 'Kp. Parasi',
                'status': 'dikirim',
            },
        )

        SetoranHafalan.objects.get_or_create(
            santri=santri_objs[0],
            jenis=SetoranHafalan.TASMI,
            tanggal=hari,
            defaults={
                'dari_juz': 1,
                'dari_halaman': 1,
                'sampai_juz': 1,
                'sampai_halaman': 20,
                'mutu': 'lancar',
                'penyimak': peg_ustadz,
            },
        )

        jenis, _ = JenisTagihan.objects.get_or_create(nama='Syahriyah', defaults={'deskripsi': 'Bulanan'})
        tagihan_lunas, _ = Tagihan.objects.get_or_create(
            santri=santri_objs[0],
            jenis=jenis,
            periode=periode,
            defaults={'jumlah': Decimal('500000'), 'jatuh_tempo': hari + timedelta(days=10)},
        )
        if tagihan_lunas.status != 'lunas' and tagihan_lunas.terbayar() == 0:
            try:
                terima_bayar(tagihan_lunas, Decimal('500000'), bendahara)
            except Exception:
                pass
        Tagihan.objects.get_or_create(
            santri=santri_objs[1],
            jenis=jenis,
            periode=periode,
            defaults={'jumlah': Decimal('500000'), 'jatuh_tempo': hari - timedelta(days=2)},
        )

        jenis_p, _ = JenisPelanggaran.objects.get_or_create(nama='Terlambat shalat', defaults={'poin': 2})
        CatatanPelanggaran.objects.get_or_create(
            santri=santri_objs[1],
            jenis=jenis_p,
            tanggal=hari,
            defaults={'sanksi': 'Nasihat', 'catatan': 'Contoh'},
        )
        Izin.objects.get_or_create(
            santri=santri_objs[0],
            jenis='pulang',
            defaults={
                'status': 'diajukan',
                'mulai': now,
                'selesai': now + timedelta(days=2),
                'alasan': 'Keperluan keluarga',
                'pemohon': wali1,
            },
        )

        self.stdout.write(self.style.SUCCESS(
            'Data contoh siap. Masuk dengan mudir/tu/bendahara/ustadz1/musyrif1/wali1/wali2/santri1, sandi sandi123.'
        ))
