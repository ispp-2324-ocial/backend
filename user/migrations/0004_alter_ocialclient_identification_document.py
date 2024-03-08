# Generated by Django 4.2.10 on 2024-03-08 11:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_ocialuser_typesfaveventtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocialclient',
            name='identification_document',
            field=models.CharField(help_text='8 números seguidos de una letra del abecedario español', max_length=9, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_identification_document', message='El documento de identificación debe contener 8 números seguidos de una letra del abecedario español exceptuando i,o,u o ñ', regex='^\\d{8}(?![IOUÑiouñ])[A-HJ-NP-Za-hj-np-z]$')]),
        ),
    ]