# Generated by Django 5.0.1 on 2024-03-04 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_paymentgatewaysettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]