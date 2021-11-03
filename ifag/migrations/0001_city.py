# -*- coding: utf-8 -*-
# pylint: skip-file
import sys

from django.core.management import call_command
from django.db import migrations, models


def load_fixture(apps, schema_editor):
    if 'test' in sys.argv:
        call_command("loaddata", "city_test")
        return True

    call_command("loaddata", "city")


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name_ascii', models.CharField(max_length=255)),
                ('uf', models.CharField(max_length=2)),
            ],
            options={
                'ordering': ['name_ascii'],
            },
        ),
        migrations.RunPython(load_fixture)
    ]
