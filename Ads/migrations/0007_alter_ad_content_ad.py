# Generated by Django 4.0.5 on 2022-10-24 20:12

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ads', '0006_response_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='content_ad',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
