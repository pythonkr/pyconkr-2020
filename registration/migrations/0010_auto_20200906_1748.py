# Generated by Django 2.2.13 on 2020-09-06 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_patron'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patron',
            name='user_code',
            field=models.CharField(max_length=20),
        ),
    ]
