# Generated by Django 2.0.5 on 2018-11-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20181117_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='_type',
            field=models.CharField(max_length=3),
        ),
    ]
