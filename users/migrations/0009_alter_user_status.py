# Generated by Django 3.2.12 on 2022-08-10 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_kyc_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('kyc', 'Kyc'), ('other', 'Other'), ('pan', 'Pan'), ('aadhar', 'Aadhar'), ('video', 'Video'), ('pending', 'Pending')], default='kyc', max_length=255),
        ),
    ]