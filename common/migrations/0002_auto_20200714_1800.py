# Generated by Django 3.0.7 on 2020-07-14 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ('id',)},
        ),
    ]