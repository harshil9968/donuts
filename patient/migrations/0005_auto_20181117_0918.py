# Generated by Django 2.0.5 on 2018-11-17 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_auto_20181117_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('_id', models.UUIDField(primary_key=True, serialize=False)),
                ('sentAt', models.DateTimeField(auto_now=True)),
                ('messageType', models.CharField(choices=[('TXT', 'TEXT'), ('DOC', 'DOCUMENT'), ('IMG', 'IMAGE'), ('AUD', 'AUDIO'), ('VID', 'VIDEO')], default='Unknown', max_length=50, null=True)),
                ('messageBody', models.TextField()),
                ('thumbnailURL', models.URLField(null=True)),
                ('attachmentDisplayName', models.CharField(max_length=100, null=True)),
                ('attachmentName', models.CharField(max_length=100, null=True)),
                ('size', models.CharField(max_length=25, null=True)),
                ('duration', models.FloatField(null=True)),
                ('mimeType', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('groupType', models.CharField(choices=[('One-to-One', 'One-to-One'), ('Many-to-Many', 'Many-to-Many')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MessageRecipient',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('sentAt', models.DateTimeField(auto_now_add=True)),
                ('isRead', models.BooleanField(default=True)),
                ('readAt', models.DateTimeField(null=True)),
                ('callbackUrl', models.URLField(null=True)),
                ('message', models.ForeignKey(on_delete=None, to='patient.Message')),
            ],
        ),
        migrations.CreateModel(
            name='MessageUserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_message_time', models.DateTimeField(null=True)),
                ('group', models.ForeignKey(on_delete=None, to='patient.MessageGroup')),
            ],
        ),
        migrations.RemoveField(
            model_name='patient',
            name='appUserId',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='createdOn',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='lastName',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='patientId',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='primaryCell',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='updatedOn',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='zip5',
        ),
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('U', 'Unknown')], default='Unknown', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='zip5',
            field=models.CharField(default=99999, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messageusergroup',
            name='user',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messagerecipient',
            name='messageUserGroup',
            field=models.ForeignKey(on_delete=None, to='patient.MessageUserGroup'),
        ),
        migrations.AddField(
            model_name='messagerecipient',
            name='recipient',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Message'),
        ),
        migrations.AlterUniqueTogether(
            name='messageusergroup',
            unique_together={('user', 'group')},
        ),
    ]
