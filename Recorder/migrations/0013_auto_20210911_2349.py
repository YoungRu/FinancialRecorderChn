# Generated by Django 3.2.7 on 2021-09-11 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recorder', '0012_alter_revenue_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expend',
            name='PriceAmount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='labour',
            name='PriceAmount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='revenue',
            name='PriceAmount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]