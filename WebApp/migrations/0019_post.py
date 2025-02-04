# Generated by Django 5.1.4 on 2025-01-22 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0018_remove_blog_detail_tags_remove_blog_detail_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
