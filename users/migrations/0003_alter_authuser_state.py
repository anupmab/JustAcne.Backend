# Generated by Django 3.2.7 on 2021-09-28 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_authuser_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='state',
            field=models.CharField(max_length=254, verbose_name='state'),
        ),
    ]
