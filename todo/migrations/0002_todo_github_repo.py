# Generated by Django 3.1.7 on 2021-04-20 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='github_repo',
            field=models.CharField(default='', max_length=256),
        ),
    ]
