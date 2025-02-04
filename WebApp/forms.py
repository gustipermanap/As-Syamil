# from django import forms
# from .models import message

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = message
#         fields = ['name', 'email', 'subject', 'message']

# WebApp/forms.py
from django import forms
from .models import message, Pendaftaran

class MessageForm(forms.ModelForm):
    class Meta:
        model = message
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email', 'required': ''}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject', 'required': ''}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Message', 'required': ''}),
        }

 

class PendaftaranForm(forms.ModelForm):
    class Meta:
        model = Pendaftaran
        fields = '__all__'  # Atau tentukan field yang ingin ditampilkan

        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
            'tgl_no_ijazah': forms.DateInput(attrs={'type': 'date'}),
            'diterima_di_sekolah': forms.DateInput(attrs={'type': 'date'}),
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap', 'required': ''}),
            'nik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIK', 'required': ''}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control', 'required': ''}),
            'nisn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NISN', 'required': ''}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tempat Lahir', 'required': ''}),
            'agama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agama', 'required': ''}),
            'no_handphone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Handphone', 'required': ''}),
            'anak_ke': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Anak Ke', 'required': ''}),
            'jumlah_saudara': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jumlah Saudara', 'required': ''}),
            'asal_sekolah': forms.Select(attrs={'class': 'form-control', 'required': ''}),
            'lama_belajar': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lama Belajar', 'required': ''}),
            'pindahan_dari_sekolah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pindahan Dari Sekolah'}),
            'alasan_pindah': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alasan Pindah'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat', 'required': ''}),
            'rt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RT', 'required': ''}),
            'rw': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RW', 'required': ''}),
            'kelurahan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kelurahan', 'required': ''}),
            'kecamatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kecamatan', 'required': ''}),
            'kota_kabupaten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kota/Kabupaten', 'required': ''}),
            'kode_pos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kode Pos', 'required': ''}),
            'nama_ayah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Ayah', 'required': ''}),
            'nama_ibu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Ibu', 'required': ''}),
            'pekerjaan_ayah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pekerjaan Ayah', 'required': ''}),
            'pekerjaan_ibu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pekerjaan Ibu', 'required': ''}),
            'pendidikan_ayah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pendidikan Ayah', 'required': ''}),
            'pendidikan_ibu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pendidikan Ibu', 'required': ''}),
            'penghasilan_bulanan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Penghasilan Bulanan', 'required': ''}),
            'ktp_ayah': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ktp_ibu': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alamat_orangtua': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat Orangtua', 'required': ''}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
