# Generated by Django 5.1.4 on 2025-01-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(3, 'Ordered'), (0, 'Recieved'), (1, 'Processed'), (2, 'Sent')], default=3),
        ),
    ]
