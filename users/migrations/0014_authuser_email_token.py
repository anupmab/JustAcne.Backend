# Generated by Django 3.2.7 on 2021-10-02 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20211001_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='email_token',
            field=models.CharField(blank=True, default='', max_length=254, verbose_name='state'),
        ),
    ]
