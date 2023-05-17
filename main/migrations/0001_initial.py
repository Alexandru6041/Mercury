# Generated by Django 4.2.1 on 2023-05-15 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('display_name', models.CharField(max_length=64)),
                ('counter', models.IntegerField()),
                ('user_token', models.CharField(default='', max_length=128)),
            ],
        ),
    ]