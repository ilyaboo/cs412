# Generated by Django 5.1.3 on 2024-11-25 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment_tracker', '0002_portfolio_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('ticker', models.CharField(max_length=10)),
                ('asset_type', models.CharField(choices=[('stock', 'Stock'), ('crypto', 'Cryptocurrency')], default='stock', max_length=15)),
            ],
        ),
    ]
