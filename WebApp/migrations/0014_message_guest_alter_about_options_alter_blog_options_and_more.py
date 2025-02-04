# Generated by Django 5.1.4 on 2025-01-16 08:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0013_blog_portfolio_portfolio_item_portfolio_tag_service_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='message_guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_message', models.CharField(blank=True, max_length=20, null=True)),
                ('description_for_message', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Guest Message',
                'verbose_name_plural': 'Guest Message',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterModelOptions(
            name='about',
            options={'ordering': ['-id'], 'verbose_name': 'About', 'verbose_name_plural': 'About'},
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-id'], 'verbose_name': 'Blog', 'verbose_name_plural': 'Blog'},
        ),
        migrations.AlterModelOptions(
            name='datasekolah',
            options={'ordering': ['-id'], 'verbose_name': 'Data Sekolah', 'verbose_name_plural': 'Data Sekolah'},
        ),
        migrations.AlterModelOptions(
            name='hero',
            options={'ordering': ['-id'], 'verbose_name': 'Hero Section', 'verbose_name_plural': 'Hero Section'},
        ),
        migrations.AlterModelOptions(
            name='portfolio',
            options={'ordering': ['-id'], 'verbose_name': 'Portfolio', 'verbose_name_plural': 'Portfolio'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-id'], 'verbose_name': 'Service', 'verbose_name_plural': 'Service'},
        ),
        migrations.AlterModelOptions(
            name='service_item',
            options={'ordering': ['-service_Item_title'], 'verbose_name': 'Service Item', 'verbose_name_plural': 'Service Item'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['-id'], 'verbose_name': 'Our Team', 'verbose_name_plural': 'Our Team'},
        ),
        migrations.AlterModelOptions(
            name='testimonial',
            options={'ordering': ['-id'], 'verbose_name': 'Testimonial', 'verbose_name_plural': 'Testimonial'},
        ),
        migrations.RenameField(
            model_name='testimonial_item',
            old_name='testimonial_Item_title',
            new_name='testimonial_Personal_departement',
        ),
        migrations.RenameField(
            model_name='testimonial_item',
            old_name='testimonial_Item_description',
            new_name='testimonial_Personal_description',
        ),
        migrations.RemoveField(
            model_name='portfolio_item',
            name='link_Item_portfolio',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='person_facebook_icon',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='person_instagram_icon',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='person_twitter_icon',
        ),
        migrations.RemoveField(
            model_name='testimonial_item',
            name='link_Item_testimonial',
        ),
        migrations.AddField(
            model_name='portfolio_item',
            name='portfolio_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='WebApp.portfolio_tag'),
        ),
        migrations.AddField(
            model_name='service_item',
            name='icon_service',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='testimonial_item',
            name='testimonial_Personal_title',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='blog_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_details/')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='WebApp.blog')),
            ],
            options={
                'verbose_name': 'Blog Detail',
                'verbose_name_plural': 'Blog Details',
                'ordering': ['-created_at'],
            },
        ),
    ]
