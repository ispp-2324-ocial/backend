# Generated by Django 4.2.10 on 2024-03-08 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="event",
            new_name="description",
        ),
    ]
