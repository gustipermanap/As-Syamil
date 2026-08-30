from django import forms

from .models import Pendaftaran, message


class MessageForm(forms.ModelForm):
    class Meta:
        model = message
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Nama',
            'email': 'Email',
            'subject': 'Subjek',
            'message': 'Pesan',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Anda'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Anda'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subjek'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Pesan'}),
        }


class PendaftaranForm(forms.ModelForm):
    class Meta:
        model = Pendaftaran
        exclude = ['created_at']
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tgl_no_ijazah': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diterima_di_sekolah': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'nik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIK', 'maxlength': '16'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'nisn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NISN', 'maxlength': '12'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tempat Lahir'}),
            'agama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agama'}),
            'no_handphone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Handphone'}),
            'anak_ke': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Anak Ke', 'min': 1}),
            'jumlah_saudara': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jumlah Saudara', 'min': 0}),
            'asal_sekolah': forms.Select(attrs={'class': 'form-control'}),
            'lama_belajar': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lama Belajar (tahun)', 'min': 0}),
            'pindahan_dari_sekolah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pindahan Dari Sekolah'}),
            'alasan_pindah': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Alasan Pindah'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Alamat'}),
            'rt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RT'}),
            'rw': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RW'}),
            'kelurahan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kelurahan'}),
            'kecamatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kecamatan'}),
            'kota_kabupaten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kota/Kabupaten'}),
            'kode_pos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kode Pos'}),
            'nama_ayah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Ayah'}),
            'nama_ibu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Ibu'}),
            'pekerjaan_ayah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pekerjaan Ayah'}),
            'pekerjaan_ibu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pekerjaan Ibu'}),
            'pendidikan_ayah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pendidikan Ayah'}),
            'pendidikan_ibu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pendidikan Ibu'}),
            'penghasilan_bulanan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Penghasilan Bulanan', 'min': 0}),
            'ktp_ayah': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ktp_ibu': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alamat_orangtua': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Alamat Orangtua'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
