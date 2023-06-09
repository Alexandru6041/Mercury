# Generated by Django 4.2.1 on 2023-05-25 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=50, unique=True)),
                ('dimensiune', models.FloatField()),
                ('sheet', models.CharField(max_length=20)),
                ('rand_header', models.IntegerField()),
                ('nume_firma', models.CharField(max_length=100)),
                ('cif_firma', models.IntegerField()),
            ],
        ),
    ]
