# Generated by Django 5.1.2 on 2024-12-30 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0007_alter_defaultpricing_sport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sport',
            name='price',
        ),
    ]
