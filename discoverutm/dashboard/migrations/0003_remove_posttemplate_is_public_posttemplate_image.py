# Generated by Django 5.1.6 on 2025-05-03 07:05

import dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posttemplate',
            name='is_public',
        ),
        migrations.AddField(
            model_name='posttemplate',
            name='image',
            field=models.ImageField(blank=True, upload_to=dashboard.models.path_and_rename, verbose_name='Image'),
        ),
    ]
