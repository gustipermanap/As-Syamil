# Generated by Django 5.1.4 on 2025-01-14 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0008_alter_hero_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(help_text="Bootstrap icon name (e.g. 'easel', 'gem')", max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('link', models.CharField(blank=True, max_length=200)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
