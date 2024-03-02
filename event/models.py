from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import OcialClient
from django.forms import ModelForm


# Create your models here.
class Event(models.Model):
    class Category(models.TextChoices):
        SPORTS = 0, ("Sports")
        MUSIC = 1, ("Music")
        MARKETS = 2, ("Markets")
        RELAX_ACTIVITIES = 3, ("Relax activities")
        LIVE_CONCERT = 4, ("Live concert")

    name = models.TextField()
    place = models.TextField()
    event = models.TextField()
    date = models.DateField()
    hour = models.TimeField()
    capacity = models.PositiveIntegerField(default=0)
    category = models.TextField(choices=Category.choices, default=Category.SPORTS)
    latitude = models.FloatField()
    longitude = models.FloatField()
    ocialClient = models.ForeignKey(
        OcialClient, related_name="OcialClient", on_delete=models.CASCADE
    )

    # def get_event_by_client(self):
    # obj = Event.objects.get(pk=self.object.id)
    # return obj

    # def get_event_with_latitud():

    def __str__(self):
        return "{}: {} | {}, {}".format(self.name, self.event, self.date, self.hour)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            self.name
            self.place
            self.event
            self.date
            self.hour
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

class OcialEventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
