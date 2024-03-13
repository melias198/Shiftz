# Generated by Django 5.0.1 on 2024-03-13 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Placed'), (4, 'Shipped'), (5, 'Delivered')], default=1),
        ),
    ]
