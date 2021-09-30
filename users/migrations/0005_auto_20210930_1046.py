# Generated by Django 3.2.7 on 2021-09-30 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='billing_address',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='authuser',
            name='checkout_info',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='authuser',
            name='shipping_address',
            field=models.JSONField(default={}),
        ),
    ]
