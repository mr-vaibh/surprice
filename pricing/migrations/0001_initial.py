# Generated by Django 5.1.2 on 2024-12-30 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PricingOverride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('override_type', models.CharField(choices=[('datetime', 'Date and Time'), ('daytime', 'Day and Time'), ('timeonly', 'Time of Day')], max_length=10)),
                ('date', models.DateField(blank=True, null=True)),
                ('day_of_week', models.IntegerField(blank=True, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('price_modifier', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricing.sport')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricing.sport')),
            ],
        ),
    ]
