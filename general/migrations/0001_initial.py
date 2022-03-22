# Generated by Django 3.2.12 on 2022-03-22 17:01

import ckeditor.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('feedback', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Guidelines',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('guideline', ckeditor.fields.RichTextField()),
                ('user_type', models.CharField(choices=[('operator', 'Operator'), ('user', 'User')], max_length=30)),
            ],
        ),
    ]