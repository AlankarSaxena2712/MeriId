# Generated by Django 3.2.12 on 2022-08-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_alter_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]