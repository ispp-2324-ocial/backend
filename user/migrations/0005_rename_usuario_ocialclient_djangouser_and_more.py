# Generated by Django 4.2.10 on 2024-03-08 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_ocialclient_identification_document'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ocialclient',
            old_name='usuario',
            new_name='djangoUser',
        ),
        migrations.RenameField(
            model_name='ocialuser',
            old_name='usuario',
            new_name='djangoUser',
        ),
    ]
