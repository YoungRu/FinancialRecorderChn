# Generated by Django 3.2.7 on 2021-09-09 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Recorder', '0008_alter_revenue_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='revenue',
            old_name='User',
            new_name='user',
        ),
    ]
