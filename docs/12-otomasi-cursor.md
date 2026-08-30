# 12 — Otomasi Cursor (agentic development)

Cursor **tidak punya antrean issue berurutan bawaan**. Automation berjalan per peristiwa. Kita memakai **label GitHub `sia-ready`** sebagai gerbang.

Agent di repo ini **tidak bisa menekan Save** di dasbor. Pemilik harus mengaktifkan automation sekali.

## Prasyarat

1. Gabungkan PR dokumen ini ke `main` (agar agent yang boot dari `main` melihat `docs/` dan `AGENTS.md`).
2. Paket Cursor berbayar + GitHub terhubung: [Integrations](https://cursor.com/dashboard?tab=integrations).
3. Environment Cloud Agent: [environment As-Syamil](https://cursor.com/dashboard/cloud-agents/environments/e/7f666d87-a42a-11f1-a7d1-d6b4613131ce) — **Save** setelah review `.cursor/environment.json`.

## Buat Automation (sekali)

Buka [cursor.com/automations/new](https://cursor.com/automations/new).

| Field | Isi |
|---|---|
| Nama | `SIA — kerjakan issue sia-ready` |
| Trigger | GitHub → **Issue label changed** → label `sia-ready` **ditambah** |
| Repository | `gustipermanap/As-Syamil`, branch `main` |
| Tools | Biarkan pembuatan PR dan Computer use aktif |
| Prompt | Tempel blok di bawah |

Lalu **Save and activate**.

### Prompt siap tempel

```
Kamu mengerjakan Sistem Akademik Pesantren As-Syamil.

Kerjakan HANYA issue GitHub yang baru mendapat label sia-ready.
1. Baca AGENTS.md, docs/09-runbook-otomasi.md, dan bagian issue itu di docs/08-katalog-issue-agent.md.
2. Jika dependensi issue belum ada di main, JANGAN menulis kode. Komentari blocker di issue, lalu berhenti.
3. Satu cabang, satu PR, judul "SIA-XXX: ringkasan".
4. Istilah UI: santri, ustadz, syahriyah, halaqah — bukan siswa/guru/SPP.
5. Jangan kerjakan SIA lain. Jangan commit env/, .env, atau db.sqlite3.
6. Jalankan tes app yang disentuh dan python manage.py check.
```

## Cara jalan tiap hari

Jangan menempel `sia-ready` ke 24 issue sekaligus (tabrakan migrasi).

1. Setelah dokumen di `main`, tempel `sia-ready` hanya pada **SIA-001**.
2. Tinjau PR agent, gabungkan ke `main`.
3. Tempel `sia-ready` ke issue berikutnya yang sudah bebas dependensi (lihat `docs/07-backlog-4-minggu.md`).
4. Ulangi sampai SIA-024.

## Alternatif tanpa Automation

Di issue GitHub, komentar:

```
@cursor Kerjakan issue ini saja. Ikuti AGENTS.md dan docs/09-runbook-otomasi.md.
```

## Label

| Label | Arti |
|---|---|
| `sia` | Semua issue akademik |
| `sia-ready` | Agent boleh mulai (pemicu automation) |
| `sia-blocked` | Menunggu issue lain |
| `week-1` … `week-4` | Slot backlog |
