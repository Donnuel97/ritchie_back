# Generated by Django 5.1 on 2024-08-17 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='admin', max_length=30, unique=True)),
                ('email', models.EmailField(default='admin', max_length=254, unique=True)),
                ('password', models.CharField(default='july1234', max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('phone_number', models.CharField(max_length=11, null=True)),
            ],
        ),
    ]
