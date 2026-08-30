# 01 — Peran dan hak akses

Semua label di antarmuka memakai istilah di tabel ini. Jangan membuat peran baru tanpa issue tersendiri.

## Peran

| Kode | Peran | Tugas |
|---|---|---|
| R01 | **Pengasuh / Mudir** | Melihat semua laporan, menyetujui kebijakan, tidak wajib input harian |
| R02 | **Tata Usaha** | Master data, PPDB, santri, cetak rapor, arsip. Jika pengaturan `pengelola_keuangan=tata_usaha`, TU juga mengelola tagihan |
| R03 | **Bendahara** | Tagihan, pembayaran, tunggakan, kwitansi. Hanya aktif jika `pengelola_keuangan=bendahara` |
| R04 | **Ustadz / Ustadzah** | Absensi dan nilai rombongan belajar yang diampu; setoran hafalan jika ditugaskan |
| R05 | **Musyrif / Pengurus asrama** | Absensi asrama, penempatan kamar, izin pulang |
| R06 | **Wali santri** | Melihat data anak, tagihan, izin, hafalan, rapor (hanya anaknya) |
| R07 | **Santri** | Melihat jadwal, hafalan sendiri, status izin (opsional; boleh ditunda jika pemilik mematikan portal santri) |
| R08 | **Calon santri** | Mengisi formulir PPDB publik, melihat status pendaftaran dengan kode |

Superuser Django tetap ada untuk instalasi awal, lalu dibatasi.

## Matriks akses (ringkas)

| Data | Mudir | TU | Bendahara | Ustadz | Musyrif | Wali | Santri |
|---|---|---|---|---|---|---|---|
| Pengaturan lembaga | Ubah | Lihat | Tidak | Tidak | Tidak | Tidak | Tidak |
| Struktur (jenjang, RB) | Lihat | Ubah | Tidak | Lihat | Lihat | Tidak | Tidak |
| PPDB | Lihat | Ubah | Tidak | Tidak | Tidak | Tidak | Daftar (publik) |
| Biodata santri | Lihat | Ubah | Lihat terbatas | Lihat kelasnya | Lihat asramanya | Anaknya | Dirinya |
| Absensi KBM | Lihat | Lihat | Tidak | Ubah | Tidak | Anaknya | Dirinya |
| Hafalan | Lihat | Lihat | Tidak | Ubah (jika ampu) | Lihat | Anaknya | Dirinya |
| Nilai / rapor | Lihat | Ubah/cetak | Tidak | Ubah mapelnya | Tidak | Anaknya | Dirinya |
| Kamar | Lihat | Ubah | Tidak | Tidak | Ubah | Anaknya | Dirinya |
| Izin | Setuju (opsional) | Ubah | Tidak | Usul | Ubah | Ajukan/lihat | Ajukan/lihat |
| Pelanggaran | Lihat | Ubah | Tidak | Usul | Ubah | Anaknya | Dirinya |
| Keuangan | Lihat | Sesuai pengaturan | Ubah | Tidak | Tidak | Tagihan anak | Tidak |
| NIK / penghasilan wali | Lihat | Ubah | Tidak | Tidak | Tidak | Dirinya | Tidak |

“Lihat terbatas” = nama, nomor induk, status, tanpa NIK dan penghasilan.

## Pengaturan peran keuangan

Di **Identitas lembaga**:

```
pengelola_keuangan = bendahara | tata_usaha
```

- `bendahara`: menu keuangan hanya R03 (+ mudir lihat)
- `tata_usaha`: menu keuangan dipegang R02; peran Bendahara disembunyikan

Default: `bendahara`.

## Portal

| Portal | URL usulan | Siapa |
|---|---|---|
| Publik | `/` | Tamu, calon santri |
| PPDB | `/ppdb/` | Calon santri |
| Masuk | `/masuk/` | Semua akun internal |
| Operasional | `/operasi/` | TU, bendahara, ustadz, musyrif, mudir |
| Wali | `/wali/` | Wali santri |
| Santri | `/santri/` | Santri (bisa dimatikan) |
| CMS lama | `/admin/` | Superuser / pengelola konten web |

Jangan memakai `/admin/` sebagai tempat input akademik harian. Admin Django hanya untuk CMS web dan perbaikan darurat.
