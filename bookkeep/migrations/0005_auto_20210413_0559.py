# Generated by Django 3.1.7 on 2021-04-13 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeep', '0004_installment_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='paynode',
            name='interest',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='paynode',
            name='principal',
            field=models.IntegerField(default=0),
        ),
    ]
