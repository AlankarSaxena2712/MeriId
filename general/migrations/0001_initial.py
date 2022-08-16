# Generated by Django 3.2.12 on 2022-08-16 19:25

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guidelines',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('guideline', ckeditor.fields.RichTextField()),
                ('user_type', models.CharField(choices=[('operator', 'Operator'), ('user', 'User'), ('admin', 'Admin')], max_length=30, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Guidelines',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='notice/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Notices',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('description', models.TextField()),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
            ],
        ),
    ]
