# Generated by Django 3.2.7 on 2021-09-26 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recorder', '0021_alter_revenue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revenue',
            name='Date',
            field=models.DateTimeField(verbose_name='Date recieved'),
        ),
    ]
