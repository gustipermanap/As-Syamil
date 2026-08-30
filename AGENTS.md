# Instruksi agent — As-Syamil

Ini website + CMS pesantren yang sedang menjadi **Sistem Akademik Pesantren**.

## Sumber kebenaran

Baca berurutan sebelum menulis kode:

1. `docs/README.md`
2. Issue GitHub yang sedang dikerjakan (judul `SIA-XXX`)
3. `docs/08-katalog-issue-agent.md` untuk issue itu
4. `docs/09-runbook-otomasi.md`
5. `docs/11-istilah.md`

Jika dokumen dan issue bentrok, ikut dokumen + komentar di issue. Jangan mengarang kebijakan baru.

## Cursor Cloud specific instructions

- Satu issue = satu cabang = satu PR. Judul PR: `SIA-XXX: ringkasan`.
- Kerjakan **hanya** issue yang mendapat label `sia-ready` atau yang disebut eksplisit di prompt.
- Jika dependensi di katalog belum ada di `main`, **jangan kode**. Komentari blocker di issue/PR.
- Jangan menjalankan SIA berikutnya “sekalian”.
- UI: istilah baku pesantren (santri, ustadz, syahriyah, halaqah). Bukan siswa/guru/SPP.
- App akademik baru sesuai `docs/05-arsitektur-teknis.md`. Jangan menumpuk semua model di `WebApp`.
- Jangan hapus CMS/website yang ada.
- Jangan commit `.env`, `env/`, `db.sqlite3`.
- Tes: `python manage.py test` untuk app yang disentuh, plus `python manage.py check`.
- Dependensi: `pip install -r requirements.txt` (Python 3.12 boleh).

## Di luar lingkup kecuali issue menyebutnya

Aplikasi genggam, QRIS/VA, EMIS/Dapodik, mesin absensi, blast WhatsApp, ganti stack.
