# Generated by Django 5.1.4 on 2025-02-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0033_remove_service_item_icon_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/'),
        ),
    ]
