# Generated by Django 5.1.4 on 2025-01-04 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]
