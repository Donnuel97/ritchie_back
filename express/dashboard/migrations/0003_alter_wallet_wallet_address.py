# Generated by Django 5.0.1 on 2024-09-16 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_userform_email_alter_userform_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
