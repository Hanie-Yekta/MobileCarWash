# Generated by Django 5.0.4 on 2024-08-22 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='serviceprice',
            unique_together=set(),
        ),
    ]
