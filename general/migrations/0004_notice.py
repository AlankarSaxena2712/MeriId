# Generated by Django 3.2.12 on 2022-08-01 16:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_alter_guidelines_guideline'),
    ]

    operations = [
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
    ]
