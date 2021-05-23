# Generated by Django 3.1.7 on 2021-05-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
        ('todo', '0005_auto_20210523_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='todo',
            name='persons',
            field=models.ManyToManyField(blank=True, default=None, to='person.Person'),
        ),
    ]
