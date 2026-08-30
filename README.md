# Website CMS Pondok Pesantren As-Syamil

Website publik dan panel CMS (Django Admin) untuk Pondok Pesantren As-Syamil, Pandeglang.

Ini **bukan** sistem akademik. Tidak ada portal siswa, absensi, nilai, keuangan, atau pembayaran. Admin mengelola konten beranda, blog, pesan tamu, dan data pendaftaran PPDB melalui `/admin/`.

## Fitur

- Beranda dinamis: hero, tentang, sponsor, ajakan, program, testimoni, galeri, pengurus, berita
- Blog / berita
- Formulir kontak
- Formulir PPDB (disimpan ke database, dilihat di admin)
- CMS lewat Django Admin + editor TinyMCE untuk isi artikel

## Menjalankan secara lokal

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env   # opsional
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Website: http://127.0.0.1:8000/
- CMS: http://127.0.0.1:8000/admin/

## Produksi

Isi variabel lingkungan dari `.env.example`:

- `DJANGO_SECRET_KEY` — kunci acak, jangan pakai nilai bawaan
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS` — domain situs, tanpa `*`
- `DJANGO_CSRF_TRUSTED_ORIGINS` — origin HTTPS situs

Jangan mengunggah `db.sqlite3`, folder `env/`, atau `.env` ke git.

## Lisensi

MIT © Gusti Permana Putra
