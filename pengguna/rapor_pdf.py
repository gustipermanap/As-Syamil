from django.http import HttpResponse


def _teks(nilai):
    return str(nilai or '').encode('latin-1', 'replace').decode('latin-1')


def buat_pdf_rapor(santri, nilai, pengaturan):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, _teks(pengaturan.nama_tampil), new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, 'Rapor santri', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 8, _teks(f'{santri.nama}  ·  {santri.nomor_induk_santri}'), new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 10)
    lebar = (50, 35, 25, 25, 55)
    kepala = ('Kitab / mapel', 'Jenis', 'Nilai', 'Predikat', 'Periode')
    for i, teks in enumerate(kepala):
        pdf.cell(lebar[i], 8, teks, border=1)
    pdf.ln()
    pdf.set_font('Helvetica', '', 10)
    if not nilai:
        pdf.cell(sum(lebar), 8, 'Belum ada nilai.', border=1, new_x='LMARGIN', new_y='NEXT')
    else:
        for n in nilai:
            baris = (
                n.mapel.nama if n.mapel_id else '',
                n.get_jenis_display(),
                str(n.nilai),
                n.predikat,
                str(n.periode) if n.periode_id else '',
            )
            for i, teks in enumerate(baris):
                pdf.cell(lebar[i], 8, _teks(teks)[:40], border=1)
            pdf.ln()
    data = pdf.output()
    if isinstance(data, str):
        data = data.encode('latin-1')
    nama = f'rapor_{santri.nomor_induk_santri}.pdf'
    response = HttpResponse(bytes(data), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nama}"'
    return response
