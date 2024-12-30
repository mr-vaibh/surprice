# Generated by Django 5.1.2 on 2024-12-30 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0006_sport_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultpricing',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_pricing', to='pricing.sport'),
        ),
    ]
