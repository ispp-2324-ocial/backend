from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import OcialClient, OcialUser
from django.forms import ModelForm
from ocial.models import *
from images.models import Image


# Create your models here.
class Event(models.Model):
    name = models.TextField()
    place = models.TextField()
    event = models.TextField()
    timeStart = models.DateTimeField(default="1030-01-01 09:00:00")
    timeEnd = models.DateTimeField(default="1030-01-01 10:00:00")
    capacity = models.PositiveIntegerField(default=0)
    category = models.TextField(
        choices=[(category.value, category.name) for category in Category],
        default=Category.SPORTS.value,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    ocialClient = models.ForeignKey(
        OcialClient, related_name="OcialClient", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        Image,
        related_name="EventImage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "{}: {} | {} -> {}".format(
            self.name, self.event, self.timeStart, self.timeEnd
        )

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            self.name
            self.place
            self.event
            self.timeStart
            self.timeEnd
            self.capacity
            self.category
            self.latitude
            self.longitude
            self.ocialClient


class Rating(models.Model):
    score = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    comment = models.TextField(blank=True, null=True)
    event = models.ForeignKey(Event, related_name="Rating", on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.score, self.comment)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            self.score
            self.comment
            self.event


class Like(models.Model):
    event = models.ForeignKey(Event, related_name="Like", on_delete=models.CASCADE)
    user = models.ForeignKey(OcialUser, related_name="Like", on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.event, self.user)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            self.event
            self.user


class OcialEventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
