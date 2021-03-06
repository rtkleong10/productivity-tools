# Generated by Django 3.0.7 on 2020-07-14 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0002_auto_20200714_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Identifies the cycle.', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the cycle is created.')),
                ('user', models.ForeignKey(help_text='The user this cycle belongs to.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Identifies the timer.', max_length=200)),
                ('duration', models.DurationField(help_text='The duration of the timer.')),
                ('color', models.ForeignKey(help_text='Colour attached to the timer.', on_delete=django.db.models.deletion.PROTECT, to='common.Color')),
                ('cycle', models.ForeignKey(help_text='The cycle the timer is for.', on_delete=django.db.models.deletion.CASCADE, related_name='timers', to='time_cycles.Cycle')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]
