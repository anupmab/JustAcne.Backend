# Generated by Django 3.2.7 on 2021-10-01 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210930_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authuser',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='authuser',
            name='role',
        ),
        migrations.AddField(
            model_name='authuser',
            name='access_type',
            field=models.CharField(choices=[('USER', 'USER'), ('ADMIN', 'ADMIN')], default='USER', max_length=20),
        ),
    ]
