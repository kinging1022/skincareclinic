# Generated by Django 5.1.4 on 2025-01-10 23:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0006_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=225, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('order_amount', models.CharField(blank=True, max_length=225, null=True)),
                ('shipping_fee', models.CharField(blank=True, max_length=225, null=True)),
                ('order_amount_with_shipping', models.CharField(blank=True, max_length=225, null=True)),
                ('delivery_method', models.CharField(choices=[('pickup', 'Pick Up'), ('delivery', 'Delivery')], default='pickup', max_length=20)),
                ('delivery_area', models.CharField(blank=True, max_length=100, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('transaction_ref', models.CharField(blank=True, editable=False, max_length=225, null=True)),
                ('shipped_date', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Ordered'), (1, 'Recieved'), (2, 'Processed'), (3, 'Sent')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(blank=True, max_length=225, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='items', to='shop.product')),
            ],
        ),
    ]
