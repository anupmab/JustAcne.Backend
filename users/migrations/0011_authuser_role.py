# Generated by Django 3.2.7 on 2021-09-30 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_authuser_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', max_length=20),
        ),
    ]
