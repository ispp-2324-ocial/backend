# Generated by Django 4.2.10 on 2024-03-01 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeSubscription', models.TextField(choices=[('0', 'Free'), ('1', 'Basic'), ('2', 'Pro')], default='0')),
                ('numEvents', models.PositiveIntegerField()),
                ('canEditEvent', models.BooleanField(default=False)),
                ('canSendNotifications', models.BooleanField(default=False)),
                ('canHaveRecurrentEvents', models.BooleanField(default=False)),
                ('canHaveOustandingEvents', models.BooleanField(default=False)),
                ('canHaveRating', models.BooleanField(default=False)),
            ],
        ),
    ]
