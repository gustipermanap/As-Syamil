# Generated by Django 5.1.4 on 2025-01-14 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0009_herobox'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HeroBox',
        ),
        migrations.AddField(
            model_name='hero',
            name='button_name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='hero',
            name='icon',
            field=models.CharField(blank=True, help_text="Bootstrap icon name (e.g. 'easel', 'gem')", max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hero',
            name='image_landing_page',
            field=models.ImageField(blank=True, null=True, upload_to='hero/'),
        ),
        migrations.AddField(
            model_name='hero',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
