# Generated by Django 3.0.5 on 2020-04-07 16:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200407_2215'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityevent',
            options={'ordering': ('date',)},
        ),
        migrations.AddField(
            model_name='activityevent',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, help_text='The date of the event.'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='activityevent',
            unique_together={('activity', 'date')},
        ),
        migrations.RemoveField(
            model_name='activityevent',
            name='date_time',
        ),
    ]
