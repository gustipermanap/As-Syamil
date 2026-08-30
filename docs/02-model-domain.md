# 02 — Model domain

Nama model di kode boleh berbahasa Inggris teknis, tetapi `verbose_name` dan UI wajib istilah pesantren.

## Diagram ringkas

```
Lembaga
 ├─ PengaturanModul
 ├─ UnitPendidikan (formal | diniyah | tahfidz | asrama)
 │    ├─ Jenjang          (nama bebas: Wustha, MTs, I'dadiyah, …)
 │    ├─ RuangBelajar     (kelas / halaqah / kelompok)
 │    └─ KitabAtauMapel
 ├─ TahunAjaran ─ Periode (semester / caturwulan — dipilih pemilik)
 ├─ RombonganBelajar (RB) = RuangBelajar + TahunAjaran + WaliKelas/Pengampu
 ├─ Pengguna ─ Peran
 ├─ Pegawai (ustadz, musyrif, staf)
 ├─ WaliSantri
 ├─ Santri
 │    ├─ KeanggotaanRB
 │    ├─ PenempatanKamar
 │    ├─ ProgressHafalan
 │    └─ Tagihan
 ├─ GelombangPPDB ─ Pendaftaran ─ (lulus) → Santri
 ├─ Jadwal ─ Pertemuan ─ Absensi
 ├─ Penilaian
 ├─ SetoranHafalan
 ├─ Izin
 ├─ Pelanggaran
 └─ Pembayaran
```

## Entitas inti

### Lembaga

Perluas `DataSekolah` yang sudah ada. Jangan buat tabel lembaga kedua.

Tambahan wajib:

- `nsm` (opsional, madrasah)
- `npsn` (opsional, formal)
- `pengelola_keuangan` (`bendahara` / `tata_usaha`)
- `portal_santri_aktif` (bool)
- `jenis_periode` (`semester` / `caturwulan`)
- modul aktif: PPDB, akademik, tahfidz, asrama, keuangan, kedisiplinan

### UnitPendidikan

Unit yang dihidupkan pemilik.

| Field | Ketentuan |
|---|---|
| nama | Contoh: Madrasah Tsanawiyah, Diniyah, Tahfidz, Asrama Putra |
| tipe | `formal` / `diniyah` / `tahfidz` / `asrama` |
| aktif | bool |
| label_peserta | default `Santri`; unit formal boleh `Siswa` jika pemilik mengisi |

### Jenjang

Nama bebas. Contoh bawaan (boleh dihapus/diubah pemilik): I'dadiyah, Ula, Wustha, Ulya, MTs, MA.

### TahunAjaran dan Periode

- Tahun ajaran: `2026/2027`, tanggal mulai–selesai, `aktif`
- Periode: mengikuti `jenis_periode` lembaga (Ganjil/Genap atau I–IV)
- Hanya satu tahun ajaran aktif

### RuangBelajar

Wadah kegiatan. Tipe: `kelas`, `halaqah`, `kelompok_tahfidz`.

### RombonganBelajar

Gabungan ruang + tahun ajaran. Memuat daftar santri dan pengampu.

### Pegawai

Ustadz/ustadzah, musyrif, staf TU, bendahara. Terhubung ke akun pengguna.

Field penting: nama, jenis kelamin, kontak, status (aktif/nonaktif), tugas.

### WaliSantri

Orang tua/wali. Satu wali bisa mengasuh beberapa santri.

Field penting: nama, hubungan, kontak, alamat, pekerjaan, penghasilan (terbatas), akun portal.

### Santri

Bukan duplikat mentah `Pendaftaran`. Pendaftaran yang lulus **menyalin** data ke Santri.

Field wajib:

- `nomor_induk_santri` (NIS internal, unik)
- `nisn` (opsional, untuk unit formal)
- nama, NIK, tempat/tanggal lahir, jenis kelamin
- status: `calon` / `aktif` / `izin_panjang` / `lulus` / `keluar` / `dikeluarkan`
- wali, foto, alamat
- asal pendaftaran (FK opsional)

### Asrama

`Gedung` → `Kamar` (kapasitas, putra/putri) → `PenempatanKamar` (santri, tanggal masuk/keluar).

### PPDB

Ganti periode teks di website menjadi gelombang:

| Field gelombang | Ketentuan |
|---|---|
| nama | Contoh: Gelombang 1 1447 H |
| mulai, selesai | datetime |
| kuota | int |
| status | `draf` / `dibuka` / `ditutup` / `seleksi` / `selesai` |
| biaya_pendaftaran | opsional |
| unit_tujuan | FK UnitPendidikan |

Status pendaftaran: `dikirim` / `berkas_kurang` / `verifikasi` / `tes` / `diterima` / `cadangan` / `ditolak` / `mengundurkan_diri`.

Model `Pendaftaran` yang ada **dipertahankan dan diperluas**, jangan dihapus.

### Absensi

Per pertemuan: `hadir` / `izin` / `sakit` / `alpa` / `terlambat`.

Sumber pertemuan: jadwal KBM, halaqah, atau absensi asrama (kegiatan malam/shalat — jika unit asrama aktif).

### Kitab / mata pelajaran

`KitabAtauMapel`: nama, unit, jenjang opsional, kkm/nilai minimum opsional, jenis `kitab` / `mapel_umum` / `mapel_diniyah`.

### Penilaian

Nilai angka 0–100 dan predikat. Jenis: harian, ujian, akhir periode. Rapor merangkum per RB dan periode.

### Tahfidz (praktik umum)

Satu santri punya `ProgressHafalan`:

- `juz_selesai` (0–30)
- `halaman_berjalan` (1–20 per juz, mushaf standar 15 baris)
- `target_juz`

Setiap `SetoranHafalan`:

| Field | Isi |
|---|---|
| jenis | `ziyadah` (tambah baru) / `murojaah` (ulang) / `tasmi` (setor utuh) |
| dari_juz, dari_halaman | mulai |
| sampai_juz, sampai_halaman | selesai |
| mutu | `lancar` / `cukup` / `kurang` |
| catatan_tajwid | teks |
| penyimak | pegawai |
| tanggal | date |

Tasmi’ juz penuh menandai juz itu selesai jika mutu bukan `kurang`.

### Izin

Jenis: pulang, sakit, keperluan, terlambat kembali. Status: `diajukan` / `disetujui` / `ditolak` / `berlangsung` / `selesai` / `terlambat`.

### Kedisiplinan

`JenisPelanggaran` (poin, kategori ringan/sedang/berat) dan `CatatanPelanggaran` (santri, tanggal, pelapor, sanksi).

### Keuangan

- `JenisTagihan`: syahriyah, daftar ulang, makan, kitab, dll. (nama bebas)
- `Tagihan`: santri, jenis, periode, jumlah, jatuh tempo, status `belum` / `sebagian` / `lunas` / `batal`
- `Pembayaran`: tagihan, jumlah, tanggal, metode (`tunai` / `transfer` / `lainnya`), nomor kwitansi, penerima (akun)

Tidak ada gerbang pembayaran otomatis di bulan 1.

## Yang tidak boleh

- Menghapus `Pendaftaran` atau data website
- Menyamakan “kelas” sebagai satu-satunya wadah (halaqah dan kamar setara sebagai struktur)
- Menyimpan penghasilan wali di laporan publik
