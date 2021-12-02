# Generated by Django 3.2.4 on 2021-07-08 19:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='image/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg'])], verbose_name='画像')),
            ],
        ),
    ]