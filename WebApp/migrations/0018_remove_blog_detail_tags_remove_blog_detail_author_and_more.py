# Generated by Django 5.1.4 on 2025-01-22 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0017_ppdb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog_detail',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='blog_detail',
            name='author',
        ),
        migrations.DeleteModel(
            name='blog',
        ),
        migrations.DeleteModel(
            name='blog_detail',
        ),
    ]
