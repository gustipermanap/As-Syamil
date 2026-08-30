# 04 — Alur pengguna

Setiap alur harus bisa diselesaikan di UI tanpa menyentuh shell Django.

## A. Calon santri mendaftar

1. Membuka `/ppdb/`.
2. Jika gelombang `dibuka`, mengisi formulir (data diri, wali, pendidikan sebelumnya, foto).
3. Menerima **kode pendaftaran**.
4. Mengecek status dengan kode + tanggal lahir.

## B. TU mengelola PPDB

1. Membuat gelombang, mengisi kuota dan tanggal, status `draf`.
2. Membuka gelombang (`dibuka`) — formulir publik hidup.
3. Menutup manual atau otomatis saat tanggal habis / kuota penuh sesuai pengaturan.
4. Melengkapi berkas, mengubah status (`berkas_kurang` → `verifikasi` → `tes`).
5. Menetapkan `diterima` / `cadangan` / `ditolak`.
6. Aksi **Jadikan santri** untuk yang diterima: pilih unit, RB awal, kamar (jika asrama), generate NIS.

## C. Awal tahun ajaran

1. TU membuat tahun ajaran dan periode, menandai aktif.
2. TU menyalin atau membuat RB, menempatkan santri, menugaskan ustadz.
3. Jika keuangan aktif: generate tagihan syahriyah massal.

## D. Hari biasa — ustadz

1. Masuk `/operasi/`.
2. Melihat RB hari ini.
3. Mengisi absensi pertemuan.
4. Mengisi nilai atau setoran hafalan (jika bertugas).

## E. Hari biasa — musyrif

1. Absensi asrama (jika diaktifkan).
2. Memproses izin pulang.
3. Mencatat pelanggaran.
4. Memindah kamar jika perlu.

## F. Bendahara atau TU (keuangan)

1. Melihat tagihan jatuh tempo dan tunggakan.
2. Menerima pembayaran, cetak/unduh kwitansi.
3. Wali melihat sisa tagihan di `/wali/`.

## G. Wali santri

1. Masuk `/wali/`.
2. Melihat anak: status, kamar, RB, absensi ringkas, hafalan, tagihan, izin.
3. Mengajukan izin (jika diizinkan pengaturan; default ya).

## H. Mudir

1. Dasbor: jumlah santri aktif, calon PPDB, tunggakan, alpa, setoran hari ini.
2. Tidak wajib input.

## I. Website publik

1. Beranda dan blog tetap dari CMS.
2. Menu PPDB memakai aturan gelombang, bukan tanggal hardcoded.
3. Tombol Login mengarah ke `/masuk/` (bukan beranda). Staf web tetap bisa ke `/admin/` untuk CMS.
