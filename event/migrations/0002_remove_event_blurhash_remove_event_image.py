# Generated by Django 4.2.10 on 2024-03-20 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="blurhash",
        ),
        migrations.RemoveField(
            model_name="event",
            name="image",
        ),
    ]
