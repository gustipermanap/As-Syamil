# 09 — Runbook otomasi (wajib dibaca agent)

## Sebelum menulis kode

1. Baca [docs/README.md](README.md) lalu issue di [08-katalog-issue-agent.md](08-katalog-issue-agent.md).
2. Baca ketergantungan. Jika issue sebelumnya belum ada di cabang dasar, **berhenti** dan laporkan blocker.
3. Pakai istilah pesantren di UI. Jangan “siswa/guru/SPP”.
4. Jangan menambah dependensi kecuali issue menyebutnya.

## Cara kerja satu issue

1. Cabang dari dasar yang disepakati (biasanya `main`).
2. Nama cabang: `cursor/sia-XXX-slug-singkat-abdf` (ikut aturan cabang lingkungan).
3. Kerjakan hanya issue itu.
4. Migrasi jika model berubah.
5. Tes sesuai kontrak issue.
6. Commit pesan: `SIA-XXX: ringkasan dalam bahasa Indonesia`.
7. Push, buka/ubah PR, isi: issue, cara uji, risiko.
8. Jangan mencampur issue lain “sekaligus”.

## Definisi selesai (global)

- `python manage.py test` lulus untuk app yang disentuh
- `python manage.py check` tanpa error
- UI yang disentuh memakai istilah baku
- Tidak merusak beranda/CMS yang tidak terkait
- Tidak commit `.env`, `env/`, `db.sqlite3`

## Jika ragu

- Aturan bisnis: ikut [03-aturan-bisnis.md](03-aturan-bisnis.md)
- Nama field/model: ikut [02-model-domain.md](02-model-domain.md)
- Layar: ikut [06-kontrak-modul.md](06-kontrak-modul.md)
- Jangan meniru sistem sekolah umum jika bertentangan dengan istilah pesantren

## Blokir yang sah

Tulis di PR dan berhenti:

- Issue fondasi belum digabung
- Migrasi bentrok
- Keputusan produk tidak ada di docs (jangan mengarang kebijakan baru)

## Paralel

Boleh paralel hanya jika katalog menyatakan tidak berbagi model. Jika ragu, serial.

## Bahasa

Komentar kode: Indonesia atau Inggris, konsisten dalam satu file. Teks pengguna: Indonesia.
