# Generated by Django 3.2.7 on 2021-10-02 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recorder', '0023_alter_revenue_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_Date', models.DateField(null=True)),
                ('Until_Date', models.DateField(null=True)),
            ],
        ),
    ]
