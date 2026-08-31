from io import BytesIO

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from openpyxl import Workbook


def nilai_atribut(obj, path):
    cur = obj
    for part in path.split('.'):
        if cur is None:
            return ''
        panggil = part.endswith('()')
        nama = part[:-2] if panggil else part
        cur = getattr(cur, nama, '')
        if panggil and callable(cur):
            cur = cur()
        elif callable(cur) and not isinstance(cur, type):
            try:
                cur = cur()
            except TypeError:
                pass
    if cur is None:
        return ''
    return cur


class DaftarFilterMixin:
    """Pagination, cari, filter cepat/lanjutan, checkbox massal, ekspor Excel sesuai filter."""

    paginate_by = 25
    search_fields = []
    exact_filters = {}
    boolean_filters = {}
    date_field = None
    cari_placeholder = 'Cari...'
    export_filename = 'data.xlsx'
    export_columns = []
    filter_fields = []
    aksi_massal_pilihan = []

    def get_filter_fields(self):
        return list(getattr(self, 'filter_fields', []) or [])

    def apply_filters(self, qs):
        q = (self.request.GET.get('q') or '').strip()
        if q and self.search_fields:
            cond = Q()
            for field in self.search_fields:
                cond |= Q(**{f'{field}__icontains': q})
            qs = qs.filter(cond)
        for get_key, lookup in self.exact_filters.items():
            val = self.request.GET.get(get_key)
            if val:
                qs = qs.filter(**{lookup: val})
        for get_key, lookup in self.boolean_filters.items():
            val = (self.request.GET.get(get_key) or '').lower()
            if val in ('1', 'true', 'ya'):
                qs = qs.filter(**{lookup: True})
            elif val in ('0', 'false', 'tidak'):
                qs = qs.filter(**{lookup: False})
        if self.date_field:
            dari = self.request.GET.get('dari')
            sampai = self.request.GET.get('sampai')
            if dari:
                qs = qs.filter(**{f'{self.date_field}__gte': dari})
            if sampai:
                qs = qs.filter(**{f'{self.date_field}__lte': sampai})
        return qs

    def get_queryset(self):
        return self.apply_filters(super().get_queryset())

    def _enrich_filter_fields(self):
        cepat, lanjutan = [], []
        terbuka = False
        for mentah in self.get_filter_fields():
            f = dict(mentah)
            current = self.request.GET.get(f.get('name'), '')
            pilihan = []
            for item in f.get('choices') or []:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    val, lab = item[0], item[1]
                else:
                    val, lab = item, item
                val = str(val)
                pilihan.append({'value': val, 'label': lab, 'selected': val == str(current)})
            f['current'] = current
            f['options'] = pilihan
            if f.get('advanced'):
                lanjutan.append(f)
                if current:
                    terbuka = True
            else:
                cepat.append(f)
        if self.request.GET.get('dari') or self.request.GET.get('sampai'):
            terbuka = True
        return cepat, lanjutan, terbuka

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        params.pop('ekspor', None)
        ctx['filter_qs'] = params.urlencode()
        if ctx.get('paginator'):
            ctx['jumlah_filter'] = ctx['paginator'].count
        else:
            ctx['jumlah_filter'] = self.get_queryset().count()
        cepat, lanjutan, terbuka = self._enrich_filter_fields()
        ctx['filter_cepat'] = cepat
        ctx['filter_lanjutan'] = lanjutan
        ctx['filter_lanjutan_terbuka'] = terbuka
        ctx['tampilkan_tanggal'] = bool(self.date_field)
        ctx['cari_placeholder'] = getattr(self, 'cari_placeholder', 'Cari...')
        ctx['aksi_massal'] = list(getattr(self, 'aksi_massal_pilihan', []) or [])
        return ctx

    def get(self, request, *args, **kwargs):
        if request.GET.get('ekspor') == 'xlsx':
            return self.ekspor_excel()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        aksi = request.POST.get('aksi_massal')
        ids = [i for i in request.POST.getlist('pilih') if i]
        if aksi and ids:
            handler = getattr(self, f'bulk_{aksi}', None)
            if handler:
                handler(ids)
            else:
                messages.error(request, 'Aksi massal tidak dikenal.')
        else:
            messages.error(request, 'Pilih baris dan aksi terlebih dahulu.')
        qs = request.GET.urlencode()
        return redirect(request.path + (f'?{qs}' if qs else ''))

    def baris_ekspor(self, obj):
        if self.export_columns:
            return [str(nilai_atribut(obj, path)) for _, path in self.export_columns]
        return [obj.pk, str(obj)]

    def ekspor_excel(self):
        qs = self.get_queryset()
        wb = Workbook()
        ws = wb.active
        ws.title = 'Data'
        headers = [h for h, _ in self.export_columns] or ['ID', 'Nama']
        ws.append(headers)
        for obj in qs:
            ws.append(self.baris_ekspor(obj))
        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        dasar = self.export_filename.replace('.xlsx', '')
        nama = timezone.now().strftime(f'{dasar}_%Y%m%d.xlsx')
        response = HttpResponse(
            buf.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = f'attachment; filename="{nama}"'
        return response
