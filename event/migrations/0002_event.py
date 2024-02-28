# Generated by Django 4.2.10 on 2024-02-23 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('place', models.TextField()),
                ('event', models.TextField()),
                ('date', models.DateField()),
                ('hour', models.TimeField()),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('category', models.TextField(choices=[('0', 'Sports'), ('1', 'Music'), ('2', 'Markets'), ('3', 'Relax activities'), ('4', 'Live concert')], default='0')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]