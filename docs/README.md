# Dokumentasi Sistem Akademik Pesantren As-Syamil

Paket ini adalah **sumber kebenaran** untuk otomasi pengerjaan. Agent tidak boleh menebak istilah, modul, atau urutan kerja di luar dokumen ini.

Baca berurutan:

| Urutan | Dokumen | Isi |
|---|---|---|
| 1 | [00-visi-dan-lingkup.md](00-visi-dan-lingkup.md) | Tujuan, keputusan pemilik, batas 1 bulan |
| 2 | [01-peran-dan-hak-akses.md](01-peran-dan-hak-akses.md) | Siapa memakai sistem |
| 3 | [02-model-domain.md](02-model-domain.md) | Entitas dan relasi |
| 4 | [03-aturan-bisnis.md](03-aturan-bisnis.md) | Aturan operasional + kepatuhan Indonesia |
| 5 | [04-alur-pengguna.md](04-alur-pengguna.md) | Alur harian pesantren |
| 6 | [05-arsitektur-teknis.md](05-arsitektur-teknis.md) | Cara membangun di atas Django yang ada |
| 7 | [06-kontrak-modul.md](06-kontrak-modul.md) | Layar, status, dan kriteria tiap modul |
| 8 | [07-backlog-4-minggu.md](07-backlog-4-minggu.md) | Jadwal 4 minggu |
| 9 | [08-katalog-issue-agent.md](08-katalog-issue-agent.md) | Issue siap dikerjakan agent |
| 10 | [09-runbook-otomasi.md](09-runbook-otomasi.md) | Cara agent mengerjakan issue |
| 11 | [10-kriteria-rilis.md](10-kriteria-rilis.md) | Definisi “siap operasional” |
| 12 | [11-istilah.md](11-istilah.md) | Kamus istilah UI |
| 13 | [12-otomasi-cursor.md](12-otomasi-cursor.md) | Cara memasang Cursor Automation |

## Keputusan yang sudah dikunci

1. Sasaran: sistem akademik pesantren **menyeluruh**, dipakai operasional harian.
2. Seluruh modul di dokumen ini masuk lingkup.
3. PPDB menjadi gerbang resmi: buka/tutup gelombang, kelola berkas, terus ke data santri.
4. Struktur pendidikan **dapat diatur pemilik** (formal, diniyah, tahfidz, asrama — bisa campur).
5. Mengikuti aturan pendidikan dan data pribadi Indonesia.
6. Hafalan mengikuti praktik umum pesantren tahfidz.
7. Keuangan wajib. Peran pengelola uang **dapat dipilih**: Bendahara atau Tata Usaha.
8. Bahasa baku pesantren, bukan istilah sekolah umum.
9. Pengerjaan oleh **agent per issue**.
10. Rilis dianggap selesai jika semua modul dapat dipakai operasional.

## Yang bukan lingkup bulan 1

Jangan dikerjakan kecuali issue baru ditulis pemilik:

- Aplikasi mobile native
- Gerbang pembayaran otomatis (VA, QRIS, e-wallet)
- Integrasi EMIS Kemenag / Dapodik
- Absensi biometrik / mesin sidik jari
- Blast WhatsApp massal
- Ganti stack (tetap Django)
