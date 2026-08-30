# 06 — Kontrak modul

Setiap modul punya **layar wajib**, **status**, dan **selesai jika**. Agent menandai issue selesai hanya jika kolom terakhir terpenuhi.

## M01 Identitas lembaga

- Layar: ubah identitas, modul aktif, peran keuangan, jenis periode, predikat nilai.
- Selesai jika: mengubah `pengelola_keuangan` memindahkan menu keuangan; mematikan unit tahfidz menyembunyikan menu setoran.

## M02 Pengguna dan hak akses

- Layar: `/masuk/`, keluar, daftar pengguna internal (TU), reset sandi oleh TU.
- Selesai jika: tiap peran masuk ke portal yang benar; wali tidak masuk `/operasi/`.

## M03 Struktur pendidikan

- Layar: CRUD unit, jenjang, ruang, tahun ajaran, periode, RB, assign pengampu.
- Selesai jika: pemilik bisa membuat jenjang bernama bebas dan RB tanpa ubah kode.

## M04 Kepegawaian

- Layar: CRUD pegawai, tautkan akun, status nonaktif.
- Selesai jika: pegawai nonaktif tidak bisa masuk.

## M05 Santri dan wali

- Layar: daftar/filter santri, detail, ubah, tautkan wali, unggah foto, ubah status.
- Selesai jika: NIS unik; NIK duplikat pada santri aktif ditolak; wali melihat hanya anaknya.

## M06 Asrama

- Layar: gedung, kamar, penempatan, riwayat pindah.
- Selesai jika: kapasitas kamar dihormati; jenis kelamin cocok; satu kamar aktif per santri.

## M07 PPDB

- Layar publik: formulir + cek status.
- Layar TU: gelombang, antrian pendaftar, ubah status, jadikan santri.
- Selesai jika: buka/tutup mengontrol form publik; lulus menghasilkan santri + wali tanpa hilangkan baris pendaftaran.

## M08 Jadwal

- Layar: jadwal mingguan per RB (hari, jam, mapel/kitab, pengampu, ruang).
- Selesai jika: ustadz melihat hanya jadwal ampuannya.

## M09 Absensi

- Layar: isi absensi per pertemuan, rekap per santri/RB.
- Selesai jika: empat status utama tersimpan; rekap alpa tampil di dasbor.

## M10 Kurikulum

- Layar: CRUD kitab/mapel, pasang ke RB.
- Selesai jika: mapel unit diniyah dan formal bisa berbeda daftar.

## M11 Penilaian dan rapor

- Layar: input nilai, rekap, unduh/cetak rapor PDF sederhana per periode.
- Selesai jika: predikat mengikuti pengaturan; wali bisa melihat rapor anak; TU mencetak.

## M12 Tahfidz

- Layar: input setoran, riwayat, rekap progress.
- Selesai jika: ziyadah/muroja’ah/tasmi’ mengikuti [03-aturan-bisnis.md](03-aturan-bisnis.md).

## M13 Perizinan

- Layar: ajukan (wali/santri/musyrif), setujui, tandai kembali, terlambat.
- Selesai jika: status berjalan sesuai alur D/E di dokumen alur.

## M14 Kedisiplinan

- Layar: jenis pelanggaran, catat, rekap poin.
- Selesai jika: riwayat tampil di profil santri (peran yang berhak).

## M15 Keuangan

- Layar: jenis tagihan, generate massal, terima bayar, kwitansi, daftar tunggakan.
- Selesai jika: peran mengikuti pengaturan lembaga; wali melihat tagihan anak; nomor kwitansi unik.

## M16 Laporan

- Layar dasbor mudir/TU: santri aktif, PPDB masuk, kehadiran hari ini, setoran hari ini, tunggakan.
- Selesai jika: angka berasal dari data nyata, bukan placeholder.

## M17 Website dan CMS

- Beranda, blog, kontak tetap.
- PPDB publik terhubung M07.
- Login staf: `/masuk/`.
- Selesai jika: CMS konten tidak rusak; tidak ada tanggal PPDB hardcoded.
