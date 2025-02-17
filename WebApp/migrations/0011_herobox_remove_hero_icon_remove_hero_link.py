# Generated by Django 5.1.4 on 2025-01-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0010_delete_herobox_hero_button_name_hero_icon_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(blank=True, help_text="Bootstrap icon name (e.g. 'easel', 'gem')", max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Hero Box',
                'verbose_name_plural': 'Hero Box',
            },
        ),
        migrations.RemoveField(
            model_name='hero',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='link',
        ),
    ]
