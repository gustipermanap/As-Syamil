# 00 — Visi dan lingkup

## Visi

Pondok Pesantren As-Syamil memakai satu sistem untuk mengelola **calon santri, santri, pengajar, kegiatan belajar, hafalan, asrama, kedisiplinan, keuangan, dan laporan** — dari pendaftaran sampai operasional harian.

Website publik tetap ada. CMS konten beranda tetap ada. Sistem akademik adalah lapisan operasional di belakangnya, bukan pengganti profil lembaga.

## Keadaan sekarang

Repositori ini adalah website + CMS Django:

- Beranda, blog, kontak, formulir PPDB
- Admin Django untuk konten
- Model `Pendaftaran` belum terhubung ke data santri
- Tidak ada tahun ajaran, rombongan belajar, absensi, nilai, hafalan, syahriyah, atau hak akses berlapis

## Sasaran 1 bulan

Semua modul di [06-kontrak-modul.md](06-kontrak-modul.md) dapat dipakai staf pesantren tanpa spreadsheet terpisah untuk urusan harian.

“Dapat dipakai” artinya:

- Data master bisa diatur pemilik (jenjang, kelas/halaqah, kamar, jenis tagihan)
- PPDB bisa dibuka, ditutup, diseleksi, dan diluluskan menjadi santri
- Absensi, setoran hafalan, nilai, izin, dan pembayaran bisa diinput hari itu juga
- Laporan ringkas bisa dibuka (santri aktif, tunggakan, progress hafalan, rekap absensi)

Bukan berarti sempurna secara hukum atau terhubung ke sistem kementerian.

## Prinsip produk

1. **Istilah baku pesantren.** Santri, wali santri, ustadz/ustadzah, pengasuh, mudir, syahriyah, halaqah, kamar, setoran, tasmi’, ziyadah, muroja’ah. Jangan memakai siswa/guru/SPP di antarmuka kecuali pemilik menambah label khusus untuk unit formal.
2. **Struktur dapat diatur.** Pemilik memilih unit yang hidup: Formal, Diniyah, Tahfidz, Asrama. Nama jenjang tidak dikunci di kode.
3. **PPDB adalah gerbang.** Formulir publik tetap ada, tetapi dikelola sebagai gelombang: kuota, buka/tutup, status berkas, kelulusan.
4. **Peran keuangan dapat dipilih.** Pengaturan lembaga: `pengelola_keuangan = bendahara | tata_usaha`.
5. **Satu santri, banyak keanggotaan.** Seorang santri bisa sekaligus di kelas formal, halaqah diniyah, kelompok tahfidz, dan kamar.
6. **Data pribadi dilindungi.** NIK, NISN, penghasilan wali, dan foto hanya untuk peran yang berwenang.
7. **Agent mengerjakan satu issue sampai selesai.** Tidak menambah modul di luar katalog.

## Modul lingkup (wajib)

| Kode | Modul | Hasil operasional |
|---|---|---|
| M01 | Identitas lembaga & pengaturan | Nama, NSM/NPSN opsional, modul aktif, peran keuangan |
| M02 | Pengguna & hak akses | Login per peran |
| M03 | Struktur pendidikan (custom) | Unit, jenjang, rombongan belajar, tahun ajaran |
| M04 | Kepegawaian | Ustadz, pengasuh, staf |
| M05 | Santri & wali | Biodata, status, wali, dokumen |
| M06 | Asrama | Gedung, kamar, penempatan |
| M07 | PPDB | Gelombang, formulir, seleksi, kelulusan |
| M08 | Jadwal | Jadwal KBM / halaqah / kegiatan |
| M09 | Absensi | Hadir, izin, sakit, alpa |
| M10 | Kurikulum & kitab/mapel | Mata pelajaran atau kitab per unit |
| M11 | Penilaian | Nilai harian, ujian, rapor |
| M12 | Tahfidz | Setoran, tasmi’, rekap juz |
| M13 | Perizinan | Izin pulang, sakit, terlambat kembali |
| M14 | Kedisiplinan | Jenis pelanggaran, poin, sanksi |
| M15 | Keuangan | Tagihan syahriyah, bayar, tunggakan, kwitansi |
| M16 | Laporan | Dasbor operasional |
| M17 | Website & CMS | Tetap jalan, PPDB publik memakai gelombang aktif |

## Di luar lingkup (fase berikutnya)

Integrasi kementerian, pembayaran daring otomatis, aplikasi genggam, mesin absensi, dan pesan massal.
