# Generated by Django 3.2.9 on 2021-11-11 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feednews',
            name='s',
            field=models.CharField(default='AAPL', max_length=10),
            preserve_default=False,
        ),
    ]