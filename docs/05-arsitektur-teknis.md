# 05 — Arsitektur teknis

## Keputusan

- Tetap **Django** (proyek `As_Syamil`).
- Website/CMS tetap di app `WebApp`.
- Sistem akademik di app baru, jangan menumpuk semua model di `WebApp`.
- SQLite boleh untuk pengembangan. Produksi: PostgreSQL (issue infrastruktur terpisah, bukan penghalang modul).
- Autentikasi: `django.contrib.auth` + grup/izin. Jangan ganti ke framework auth lain di bulan 1.
- UI operasional: template Django + Bootstrap 5 yang sudah ada. Bukan SPA.

## App yang harus dibuat

| App | Isi |
|---|---|
| `WebApp` | Website, blog, kontak, halaman PPDB publik (memakai API/model akademik) |
| `lembaga` | Identitas, pengaturan, unit, jenjang, tahun ajaran |
| `pengguna` | Profil, peran, portal masuk |
| `kesiswaan` | Santri, wali, asrama, izin, pelanggaran |
| `ppdb` | Gelombang, perluasan `Pendaftaran` (boleh pindah model ke app ini lewat migrasi bertahap) |
| `akademik` | RB, jadwal, absensi, kitab/mapel, nilai, rapor |
| `tahfidz` | Progress dan setoran |
| `keuangan` | Jenis tagihan, tagihan, pembayaran |

Jangan membuat app di luar daftar ini.

## Pindahan PPDB

1. Issue awal: tetap pakai `WebApp.Pendaftaran`, tambah FK gelombang dan status.
2. Issue belakangan: pindahkan model ke `ppdb` hanya jika migrasi data aman dan tes lulus.
3. Formulir publik wajib `enctype` untuk foto dan menolak submit saat gelombang tertutup.

## Lapisan kode

```
models → services (aturan bisnis) → views/forms → templates
```

Aturan “jadikan santri”, “generate tagihan”, “tutup gelombang” hidup di `services`, bukan di template dan bukan di sinyal tersembunyi.

## Hak akses teknis

- Grup Django: `mudir`, `tata_usaha`, `bendahara`, `ustadz`, `musyrif`, `wali`, `santri`.
- Mixin/decorator per portal.
- Query selalu disaring: ustadz hanya RB-nya, wali hanya anaknya.

## Tes wajib per issue

- Tes model/aturan (buka/tutup PPDB, pembayaran tidak melebihi sisa, tasmi’ menandai juz).
- Tes akses (wali tidak melihat santri lain).
- Tes halaman status 200 untuk peran yang berhak, 302/403 untuk yang tidak.

## Keamanan

- Secret dan `DEBUG` dari lingkungan (jangan hardcode baru).
- Data sensitif tidak di endpoint publik.
- Unggahan foto: jenis gambar, ukuran wajar.
- CSRF tetap aktif.

## Yang dilarang agent

- Menambah React/Vue, Docker wajib, microservice, atau ganti database di tengah modul.
- Commit `env/`, `db.sqlite3`, `.env`.
- Menghapus konten CMS atau media yang ada.
