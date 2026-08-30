# 03 — Aturan bisnis dan kepatuhan Indonesia

Dokumen ini **bukan nasihat hukum**. Agent mengikuti aturan produk di bawah. Perubahan kebijakan hanya oleh pemilik.

## Bahasa dan label

- Antarmuka, email, PDF: bahasa Indonesia, istilah pesantren.
- Unit bertipe `formal` boleh menampilkan label tambahan (MTs/MA, NISN) tanpa mengganti kata “santri” secara global.
- Mata pelajaran umum tetap boleh bernama sesuai kurikulum, tetapi peserta disebut santri.

## Struktur dapat diatur

1. Pemilik mengaktifkan unit. Modul terkait ikut:
   - `formal` atau `diniyah` hidupkan akademik (jadwal, absensi KBM, nilai)
   - `tahfidz` hidupkan setoran dan rekap juz
   - `asrama` hidupkan kamar, musyrif, absensi asrama
   - keuangan dan PPDB selalu bisa diaktifkan terpisah
2. Nama jenjang, ruang, dan jenis tagihan **tidak hardcoded**.
3. Satu santri boleh punya banyak keanggotaan RB dan satu kamar aktif.
4. Santri putra hanya di kamar putra; putri hanya di kamar putri.

## PPDB

1. Formulir publik hanya menerima isian jika ada gelombang berstatus `dibuka` dan sekarang berada di antara tanggal mulai–selesai.
2. Jika tidak ada gelombang terbuka, halaman PPDB menampilkan “Pendaftaran ditutup” + periode berikutnya jika ada.
3. TU dapat menutup gelombang sebelum tanggal selesai (kuota penuh atau kebijakan).
4. Status `diterima` + aksi “jadikan santri” membuat record Santri, nomor induk, dan menautkan wali. Tidak menimpa pendaftaran lama.
5. Calon melihat status dengan **kode pendaftaran** + tanggal lahir, tanpa akun.
6. NIK dan NISN divalidasi panjang (16 dan 10–12 digit) sesuai isian umum di Indonesia. Duplikat NIK pada santri aktif ditolak.

## Tahun ajaran

- Transaksi akademik (absensi, nilai, setoran yang masuk rapor, tagihan periode) terikat tahun ajaran aktif.
- Kenaikan/kelulusan adalah aksi TU di akhir periode: pindah RB atau status `lulus`.

## Absensi dan nilai

- Ustadz hanya mengisi RB yang diampu.
- Alpa beruntun (ambang diatur lembaga, default 3 pertemuan) memunculkan peringatan di dasbor, bukan hukuman otomatis.
- Skala nilai 0–100. Predikat default: A (90–100), B (80–89), C (70–79), D (60–69), E (<60). Pemilik boleh mengubah batas di pengaturan.
- KKM/nilai minimum per mapel opsional.

## Tahfidz (praktik umum)

- Ziyadah menambah progres jika mutu `lancar` atau `cukup`.
- Mutu `kurang` tercatat tetapi tidak menambah halaman selesai.
- Tasmi’ 1 juz dengan mutu bukan `kurang` menandai juz selesai.
- Muroja’ah tidak menambah juz baru.
- Rekap ditampilkan: juz selesai, halaman berjalan, setoran 7 hari terakhir.

## Izin dan kedisiplinan

- Izin pulang melewati musyrif (asrama aktif) atau TU (asrama mati).
- Keterlambatan kembali mengubah status `terlambat` dan boleh menambah catatan pelanggaran jika disetel.
- Poin pelanggaran hanya informatif + riwayat sanksi. Tidak ada “dropout otomatis”.

## Keuangan

- Tagihan boleh digenerate massal per RB / seluruh santri aktif untuk satu jenis dan periode.
- Pembayaran tidak boleh melebihi sisa tagihan.
- Kwitansi bernomor unik, tidak dihapus (batal = status batal, arsip tetap).
- Wali melihat tagihan anaknya saja.
- Menu keuangan mengikuti `pengelola_keuangan`.

## Kepatuhan Indonesia (produk)

Acuan yang harus tercermin di data dan proses, tanpa klaim sertifikasi:

| Acuan | Dampak di sistem |
|---|---|
| UU 18/2019 tentang Pesantren | Lembaga pesantren sebagai satuan; data santri dan pendidikan pesantren setara dicatat |
| Pendidikan formal/madrasah (ketentuan Kemenag / Kemendikdasmen yang berlaku) | Field NISN, NSM/NPSN opsional; rapor unit formal bisa memakai template “madrasah/sekolah” yang dipilih pemilik |
| EMIS / Dapodik | **Tidak diintegrasikan bulan 1.** Siapkan field yang lazim (NISN, NIK, ibu kandung, rombel) agar ekspor nanti mungkin |
| UU 27/2022 PDP | Izin akses data, log akses data sensitif, foto dan NIK tidak publik, hak wali melihat data anak |
| Identitas kependudukan | NIK 16 digit; validasi format, bukan ke Dukcapil |

Agent **jangan** menulis salinan pasal undang-undang di UI. Cukup kebijakan privasi singkat di portal wali/PPDB: data dipakai untuk penerimaan dan pendidikan, tidak dipublikasikan.

## Retensi dan hapus

- Santri `keluar` / `lulus` tidak dihapus fisik.
- Pendaftaran tidak dihapus.
- Hapus fisik hanya superuser + issue khusus (bukan alur biasa).
