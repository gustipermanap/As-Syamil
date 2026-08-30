from tahfidz.models import ProgressHafalan, SetoranHafalan


def catat_setoran(setoran: SetoranHafalan):
    """Perbarui progress sesuai aturan ziyadah / muroja’ah / tasmi’."""
    progress, _ = ProgressHafalan.objects.get_or_create(santri=setoran.santri)
    if setoran.mutu == 'kurang':
        return progress
    if setoran.jenis == SetoranHafalan.MUROJAAH:
        return progress
    if setoran.jenis == SetoranHafalan.TASMI:
        progress.juz_selesai = max(progress.juz_selesai, setoran.sampai_juz)
        progress.halaman_berjalan = 1
        progress.save(update_fields=['juz_selesai', 'halaman_berjalan'])
        return progress
    if setoran.jenis == SetoranHafalan.ZIYADAH:
        halaman = setoran.sampai_halaman
        juz = setoran.sampai_juz
        if halaman >= 20:
            progress.juz_selesai = max(progress.juz_selesai, juz)
            progress.halaman_berjalan = 1
        else:
            progress.juz_selesai = max(progress.juz_selesai, max(juz - 1, 0))
            progress.halaman_berjalan = halaman
        progress.save(update_fields=['juz_selesai', 'halaman_berjalan'])
    return progress
