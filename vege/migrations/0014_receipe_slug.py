# Generated by Django 5.0.1 on 2024-01-23 16:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0013_student_is_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipe',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2024, 1, 23, 16, 36, 5, 634067, tzinfo=datetime.timezone.utc), unique=True),
            preserve_default=False,
        ),
    ]
