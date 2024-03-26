# Generated by Django 4.2.10 on 2024-03-26 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.es.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OcialUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "auth_provider",
                    models.TextField(
                        choices=[("email", "EMAIL"), ("google", "GOOGLE")],
                        default="email",
                    ),
                ),
                ("lastKnowLocLat", models.FloatField()),
                ("lastKnowLocLong", models.FloatField()),
                (
                    "djangoUser",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OcialClient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                (
                    "identificationDocument",
                    localflavor.es.models.ESIdentityCardNumberField(max_length=9),
                ),
                (
                    "typeClient",
                    models.TextField(
                        choices=[
                            ("Small business", "SMALL_BUSINESS"),
                            ("Artist", "ARTIST"),
                            ("Bar Restaurant", "BAR_RESTAURANT"),
                            ("Local Guide", "LOCAL_GUIDE"),
                            ("Events And Concerts", "EVENTS_AND_CONCERTS"),
                        ],
                        default="Small business",
                    ),
                ),
                ("defaultLatitude", models.FloatField()),
                ("defaultLongitude", models.FloatField()),
                (
                    "djangoUser",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ClientImage",
                        to="images.image",
                    ),
                ),
            ],
        ),
    ]
