# Generated by Django 4.2.10 on 2024-03-10 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_ocialuser_auth_provider"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ocialuser",
            name="typesfavEventType",
        ),
    ]