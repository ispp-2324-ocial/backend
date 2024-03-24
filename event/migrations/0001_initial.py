# Generated by Django 4.2.10 on 2024-03-24 17:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("place", models.TextField()),
                ("description", models.TextField()),
                ("date", models.DateField()),
                ("hour", models.TimeField()),
                ("capacity", models.PositiveIntegerField(default=0)),
                (
                    "category",
                    models.TextField(
                        choices=[
                            ("Sports", "SPORTS"),
                            ("Music", "MUSIC"),
                            ("Markets", "MARKETS"),
                            ("Relax activities", "RELAX_ACTIVITIES"),
                            ("Live concert", "LIVE_CONCERT"),
                        ],
                        default="Sports",
                    ),
                ),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
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
                    "score",
                    models.PositiveIntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                ("comment", models.TextField(blank=True, null=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Rating",
                        to="event.event",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
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
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Like",
                        to="event.event",
                    ),
                ),
            ],
        ),
    ]
