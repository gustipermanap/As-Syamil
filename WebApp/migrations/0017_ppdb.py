# Generated by Django 5.1.4 on 2025-01-18 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0016_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='PPDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('date_of_birth', models.DateField()),
                ('parent_name', models.CharField(max_length=100)),
                ('parent_contact', models.CharField(max_length=15)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('birth_certificate', models.FileField(blank=True, null=True, upload_to='birth_certificates/')),
                ('parent_id_card', models.FileField(blank=True, null=True, upload_to='id_cards/')),
                ('recent_photo', models.FileField(blank=True, null=True, upload_to='photos/')),
            ],
        ),
    ]
