# Generated by Django 3.2.7 on 2021-09-08 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recorder', '0005_alter_revenue_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='expend',
            name='Doc',
            field=models.FileField(blank=True, null=True, upload_to='proof/'),
        ),
    ]