# Generated by Django 5.1.3 on 2024-12-07 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment_tracker', '0004_remove_purchasedasset_asset_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasedasset',
            name='purchase_price',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
