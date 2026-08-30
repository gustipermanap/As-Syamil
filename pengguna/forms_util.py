from django import forms


def kelas_bootstrap(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect, forms.FileInput, forms.ClearableFileInput)):
            if isinstance(widget, (forms.FileInput, forms.ClearableFileInput)):
                widget.attrs.setdefault('class', 'form-control')
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-check-input')
        else:
            widget.attrs.setdefault('class', 'form-control')
    return form
