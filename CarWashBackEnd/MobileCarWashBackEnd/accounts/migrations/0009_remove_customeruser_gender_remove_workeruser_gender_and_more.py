# Generated by Django 5.1.1 on 2024-09-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_workeruser_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeruser',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='workeruser',
            name='gender',
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('female', 'female'), ('male', 'male')], max_length=10, null=True),
        ),
    ]
