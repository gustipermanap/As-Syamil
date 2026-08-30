# 07 — Backlog 4 minggu

Asumsi: beberapa agent bisa paralel **hanya** pada issue yang tidak berbagi model yang sama. Urutan di bawah adalah ketergantungan. Nomor issue ada di [08-katalog-issue-agent.md](08-katalog-issue-agent.md).

Satu bulan = 4 minggu kerja. Setiap issue wajib PR sendiri.

## Minggu 1 — Fondasi

Tujuan: lembaga, peran, struktur custom, pegawai, santri/wali bisa diisi.

| Urutan | Issue | Ketergantungan |
|---|---|---|
| 1 | SIA-001 App dan pengaturan lembaga | — |
| 2 | SIA-002 Masuk, grup, portal | SIA-001 |
| 3 | SIA-003 Unit, jenjang, tahun ajaran, RB | SIA-001 |
| 4 | SIA-004 Pegawai | SIA-002 |
| 5 | SIA-005 Wali dan santri | SIA-003, SIA-004 |

Paralel setelah SIA-001: SIA-002 dan SIA-003.

## Minggu 2 — Gerbang dan hunian

Tujuan: PPDB operasional, asrama, website memakai gelombang.

| Urutan | Issue | Ketergantungan |
|---|---|---|
| 6 | SIA-006 Gelombang PPDB | SIA-001 |
| 7 | SIA-007 Formulir publik + cek status | SIA-006 |
| 8 | SIA-008 Seleksi dan jadikan santri | SIA-005, SIA-007 |
| 9 | SIA-009 Asrama dan kamar | SIA-005 |
| 10 | SIA-010 Izin | SIA-005, SIA-009 |

## Minggu 3 — Kegiatan belajar

Tujuan: jadwal, absensi, kitab, nilai, tahfidz.

| Urutan | Issue | Ketergantungan |
|---|---|---|
| 11 | SIA-011 Kitab/mapel | SIA-003 |
| 12 | SIA-012 Jadwal | SIA-004, SIA-011 |
| 13 | SIA-013 Absensi | SIA-012, SIA-005 |
| 14 | SIA-014 Nilai | SIA-011, SIA-005 |
| 15 | SIA-015 Rapor | SIA-014 |
| 16 | SIA-016 Tahfidz | SIA-005, SIA-004 |

SIA-016 paralel dengan SIA-014 jika SIA-005 selesai.

## Minggu 4 — Uang, disiplin, dasbor, rilis

Tujuan: operasional utuh.

| Urutan | Issue | Ketergantungan |
|---|---|---|
| 17 | SIA-017 Jenis tagihan dan generate | SIA-001, SIA-005 |
| 18 | SIA-018 Pembayaran dan kwitansi | SIA-017, SIA-002 |
| 19 | SIA-019 Portal wali (baca + izin + tagihan) | SIA-005, SIA-010, SIA-018 |
| 20 | SIA-020 Kedisiplinan | SIA-005 |
| 21 | SIA-021 Dasbor laporan | SIA-008, SIA-013, SIA-016, SIA-018 |
| 22 | SIA-022 Portal santri opsional | SIA-019 |
| 23 | SIA-023 Penguatan keamanan dan privasi | SIA-002 |
| 24 | SIA-024 Ujicoba operasional ujung ke ujung | semua di atas |

## Aturan waktu

- Jika suatu issue menghambat hari berikutnya, agent berikutnya **jangan** mengarang jalan pintas. Tulis blocker di PR.
- Jangan menarik issue minggu 3 sebelum SIA-005 masuk `main` atau branch dasar yang disepakati.
- SIA-024 tidak boleh diganti demo palsu: harus alur A–H di dokumen alur.
