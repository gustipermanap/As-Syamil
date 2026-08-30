# 10 — Kriteria rilis operasional

Rilis bulan 1 diterima jika semua kotak ini benar. SIA-024 wajib menempelkan hasilnya.

## Gerbang dan data

- [ ] Gelombang PPDB bisa dibuka dan ditutup; form publik patuh
- [ ] Calon mendapat kode dan bisa cek status
- [ ] Pendaftar diterima menjadi santri; NIS terbit; baris pendaftaran tetap
- [ ] Struktur jenjang/RB/kamar bisa diatur tanpa ubah kode
- [ ] Satu santri bisa di lebih dari satu RB

## Operasional harian

- [ ] Ustadz mengisi absensi RB-nya
- [ ] Setoran tahfidz ziyadah / muroja’ah / tasmi’ berjalan sesuai aturan
- [ ] Nilai masuk dan rapor satu periode bisa dibuka/cetak
- [ ] Izin pulang bisa diajukan dan diselesaikan
- [ ] Pelanggaran tercatat di profil
- [ ] Tagihan massal dan pembayaran + kwitansi berjalan
- [ ] Menu keuangan sesuai Bendahara atau Tata Usaha

## Portal dan keamanan

- [ ] Peran masuk ke portal yang benar
- [ ] Wali hanya melihat anaknya
- [ ] NIK tidak tampil di halaman publik
- [ ] Website/CMS beranda dan blog masih berfungsi
- [ ] Tidak ada tanggal PPDB hardcoded

## Data contoh untuk serah terima

Siapkan (boleh management command `seed_operasi`):

- 1 lembaga, 2 unit (contoh: Diniyah + Tahfidz + Asrama)
- 1 tahun ajaran aktif
- 2 ustadz, 1 musyrif, 1 TU, 1 bendahara, 1 mudir, 2 wali
- 5 santri (campur putra/putri)
- 1 gelombang PPDB
- 1 RB, 1 kamar terisi
- beberapa absensi, 1 setoran, 1 tagihan lunas, 1 tunggakan

Tanpa data ini, rilis dianggap belum bisa dioperasikan.
