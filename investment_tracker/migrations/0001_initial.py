# Generated by Django 5.1.3 on 2024-11-25 05:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='investment_tracker_profiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_name', models.CharField(default='My Portfolio', max_length=100)),
                ('portfolio_creation_time', models.DateTimeField(auto_now_add=True)),
                ('portfolio_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investment_tracker.profile')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_name', models.CharField(max_length=100)),
                ('purchase_time', models.DateTimeField(auto_now_add=True)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_quantity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='investment_tracker.portfolio')),
            ],
        ),
    ]