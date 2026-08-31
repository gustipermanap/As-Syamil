from django.contrib import messages

from .forms_util import kelas_bootstrap


class UbahUmumMixin:
    """UpdateView operasional: Bootstrap, judul, pesan sukses."""

    template_name = 'pengguna/form_umum.html'
    judul = None
    enctype = None

    def get_form(self, form_class=None):
        return kelas_bootstrap(super().get_form(form_class))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['judul'] = self.judul or f'Ubah {self.object}'
        if self.enctype:
            ctx['enctype'] = self.enctype
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Data disimpan.')
        return super().form_valid(form)
