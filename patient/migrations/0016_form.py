# Generated by Django 2.0.5 on 2018-11-18 00:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_messages_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formType', models.CharField(max_length=20)),
                ('status', models.CharField(default='SUBMITTED', max_length=20)),
                ('createdBy', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
