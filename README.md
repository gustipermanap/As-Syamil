# Pondok Pesantren As-Syamil

Website publik, CMS, dan **Sistem Akademik Pesantren** untuk Pondok Pesantren As-Syamil, Pandeglang.

Keputusan produk, modul, backlog, dan aturan agent ada di [docs/README.md](docs/README.md).

## Yang sudah ada

- Website publik: beranda, program, galeri, pengurus, blog, kontak
- Formulir PPDB publik yang patuh gelombang (buka/tutup)
- CMS konten lewat Django Admin + TinyMCE (`/admin/`)
- Portal operasional (`/masuk/`, `/operasi/`, `/wali/`, `/santri/`)
- Modul: lembaga, pengguna, kesiswaan, PPDB, akademik, tahfidz, keuangan

## Menjalankan secara lokal

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env   # opsional
python manage.py migrate
python manage.py seed_operasi   # data contoh operasional
python manage.py createsuperuser
python manage.py runserver
```

- Website: http://127.0.0.1:8000/
- Masuk staf / wali / santri: http://127.0.0.1:8000/masuk/
- CMS web: http://127.0.0.1:8000/admin/

Akun contoh dari `seed_operasi` memakai sandi `sandi123` (mudir, tu, bendahara, ustadz1, musyrif1, wali1, wali2).

## Produksi

Isi variabel lingkungan dari `.env.example`:

- `DJANGO_SECRET_KEY` — kunci acak, jangan pakai nilai bawaan
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS` — domain situs, tanpa `*`
- `DJANGO_CSRF_TRUSTED_ORIGINS` — origin HTTPS situs

Jangan mengunggah `db.sqlite3`, folder `env/`, atau `.env` ke git.

## Lisensi

MIT © Gusti Permana Putra
