# Generated by Django 5.2.2 on 2025-06-10 06:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpoint', '0002_remove_userprofile_address_userprofile_user_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='part',
            name='seller',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='parts', to=settings.AUTH_USER_MODEL),
        ),
    ]
