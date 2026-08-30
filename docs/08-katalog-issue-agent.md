# 08 — Katalog issue untuk agent

Kerjakan **satu issue per cabang per PR**. Judul PR = `SIA-XXX: ringkasan`.

Setiap issue memakai definisi selesai di bawah **plus** [09-runbook-otomasi.md](09-runbook-otomasi.md).

---

## SIA-001 — App dasar dan pengaturan lembaga

**Modul:** M01  
**Lakukan:**

- Buat app `lembaga` terdaftar di `INSTALLED_APPS`.
- Perluas identitas lembaga (dari `DataSekolah` atau model `Lembaga` satu-satu yang menjadi sumber: pilih satu, jangan dua sumber).
- Field: `pengelola_keuangan`, `portal_santri_aktif`, `jenis_periode`, NSM/NPSN opsional, bendera modul.
- Layar TU/mudir: form pengaturan.

**Jangan:** mengubah tampilan beranda kecuali perlu tautan menu.

**Selesai jika:** tes mengubah `pengelola_keuangan`; `migrate` bersih; admin/operasi menampilkan pengaturan.

---

## SIA-002 — Masuk, grup, portal

**Modul:** M02  
**Lakukan:** `/masuk/`, keluar, middleware/mixin portal `/operasi/`, buat grup peran, user staff contoh di tes.

**Jangan:** custom user model kecuali terpaksa (lebih baik `OneToOne` profil).

**Selesai jika:** tes login tiap grup; wali ditolak dari `/operasi/`; tombol login web mengarah ke `/masuk/`.

---

## SIA-003 — Struktur custom

**Modul:** M03  
**Lakukan:** model Unit, Jenjang, TahunAjaran, Periode, RuangBelajar, RombonganBelajar; CRUD TU; seed contoh bisa dihapus.

**Selesai jika:** tes membuat unit+jenjang bernama bebas; satu tahun ajaran aktif.

---

## SIA-004 — Pegawai

**Modul:** M04  
**Lakukan:** model Pegawai, taut akun, nonaktifkan = tidak login.

**Selesai jika:** tes pegawai nonaktif gagal masuk.

---

## SIA-005 — Santri dan wali

**Modul:** M05  
**Lakukan:** model WaliSantri, Santri, keanggotaan RB; validasi NIK/NIS; filter daftar.

**Selesai jika:** tes NIS unik, NIK dobel ditolak, keanggotaan banyak RB.

---

## SIA-006 — Gelombang PPDB

**Modul:** M07  
**Lakukan:** model Gelombang, status, kuota, cron/tidak perlu cron: tutup berdasarkan waktu saat request.

**Selesai jika:** tes transisi status; gelombang di luar tanggal tidak `dibuka` efektif.

---

## SIA-007 — Formulir publik dan cek status

**Modul:** M07, M17  
**Lakukan:** sambungkan `Pendaftaran` ke gelombang; form mati jika tutup; kode pendaftaran; halaman cek status; `enctype` foto.

**Jangan:** script `php-email-form` yang mencegat POST.

**Selesai jika:** tes POST saat tutup gagal; saat buka berhasil; cek status dengan kode.

---

## SIA-008 — Seleksi dan jadikan santri

**Modul:** M07, M05  
**Lakukan:** antrian TU, ubah status, aksi service `terima_menjadi_santri`.

**Selesai jika:** tes data pendaftaran tersalin, NIS terbentuk, pendaftaran tetap ada.

---

## SIA-009 — Asrama

**Modul:** M06  
**Lakukan:** Gedung, Kamar, Penempatan; validasi kapasitas dan jenis kelamin.

**Selesai jika:** tes tolak kamar penuh dan salah jenis kelamin.

---

## SIA-010 — Izin

**Modul:** M13  
**Lakukan:** model + alur status; layar musyrif/TU.

**Selesai jika:** tes alur diajukan → disetujui → selesai / terlambat.

---

## SIA-011 — Kitab dan mapel

**Modul:** M10  
**Lakukan:** CRUD, pasang ke RB.

**Selesai jika:** tes mapel berbeda per unit.

---

## SIA-012 — Jadwal

**Modul:** M08  
**Lakukan:** slot mingguan; tampilan ustadz tersaring.

**Selesai jika:** tes query ustadz hanya melihat ampuan.

---

## SIA-013 — Absensi

**Modul:** M09  
**Lakukan:** pertemuan dari jadwal atau buat manual; isi massal satu RB; rekap.

**Selesai jika:** tes simpan status hadir/izin/sakit/alpa.

---

## SIA-014 — Nilai

**Modul:** M11  
**Lakukan:** input nilai per mapel/santri/jenis; predikat dari pengaturan.

**Selesai jika:** tes predikat sesuai batas.

---

## SIA-015 — Rapor

**Modul:** M11  
**Lakukan:** halaman rapor + PDF sederhana (WeasyPrint atau library yang sudah biasa; jika dependensi berat, HTML cetak dulu + issue catatan).

**Selesai jika:** TU unduh rapor satu santri satu periode; wali bisa melihat.

---

## SIA-016 — Tahfidz

**Modul:** M12  
**Lakukan:** progress + setoran; aturan ziyadah/muroja’ah/tasmi’.

**Selesai jika:** tes tasmi’ juz menandai selesai; mutu kurang tidak menambah progres.

---

## SIA-017 — Tagihan

**Modul:** M15  
**Lakukan:** jenis tagihan, generate massal ke santri aktif / RB.

**Selesai jika:** tes jumlah baris tagihan = jumlah sasaran; tidak dobel jenis+periode+santri.

---

## SIA-018 — Pembayaran dan kwitansi

**Modul:** M15  
**Lakukan:** bayar, sisa, nomor kwitansi, batasi peran sesuai pengaturan.

**Selesai jika:** tes tolak kelebihan bayar; tes menu hilang dari ustadz.

---

## SIA-019 — Portal wali

**Modul:** M05, M13, M15  
**Lakukan:** `/wali/` ringkasan anak, tagihan, izin, hafalan/absensi ringkas jika sudah ada.

**Selesai jika:** tes isolasi antarwali.

---

## SIA-020 — Kedisiplinan

**Modul:** M14  
**Lakukan:** jenis + catatan + poin di profil.

**Selesai jika:** tes poin terakumulasi.

---

## SIA-021 — Dasbor

**Modul:** M16  
**Lakukan:** kartu angka nyata untuk mudir/TU.

**Selesai jika:** tes angka mengikuti fixture.

---

## SIA-022 — Portal santri

**Modul:** M02  
**Lakukan:** `/santri/` jika `portal_santri_aktif`; jika mati, URL 404/redirect.

**Selesai jika:** tes bendera pengaturan.

---

## SIA-023 — Privasi dan penguatan

**Modul:** M02  
**Lakukan:** batasi NIK di template; kebijakan privasi singkat PPDB/wali; jangan log data sensitif.

**Selesai jika:** tes halaman publik tidak memuat NIK.

---

## SIA-024 — Ujicoba ujung ke ujung

**Modul:** semua  
**Lakukan:** tes integrasi atau skrip/manajemen command yang menjalankan alur A–H dengan data contoh. Perbaiki lubang yang ketemu. Jangan menambah fitur baru.

**Selesai jika:** alur A–H hijau; daftar cek [10-kriteria-rilis.md](10-kriteria-rilis.md) tercentang di deskripsi PR.
