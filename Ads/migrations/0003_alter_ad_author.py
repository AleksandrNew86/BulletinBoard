# Generated by Django 4.0.5 on 2022-10-22 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ads', '0002_alter_category_name_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='author',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
