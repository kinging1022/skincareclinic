# Generated by Django 5.1.4 on 2025-01-03 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
