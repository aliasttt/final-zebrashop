# Generated by Django 5.1.1 on 2024-10-27 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zebrashopapp', '0008_rename_customer_order_user_remove_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
