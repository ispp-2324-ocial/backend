from django.db import models
from django.contrib.auth.models import User
from localflavor.es.models import ESIdentityCardNumberField
from django.forms import ModelForm
from subscription.models import Subscription


class OcialUser(models.Model):
    class TypesfavEvent(models.TextChoices):
        SPORTS = 0, ("Sports")
        MUSIC = 1, ("Music")
        MARKETS = 2, ("Markets")
        RELAX_ACTIVITIES = 3, ("Relax activities")
        LIVE_CONCERTS = 4, ("Live concerts")

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    lastKnowLocLat = models.FloatField()
    lastKnowLocLong = models.FloatField()
    typesfavEventType = models.TextField(
        choices=TypesfavEvent.choices, default=TypesfavEvent.SPORTS
    )

    def __str__(self):
        return self.usuario.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OcialClient(models.Model):
    class TypeClient(models.TextChoices):
        SMALL_BUSINESS = 0, ("Small business")
        ARTIST = 1, ("Artist")
        BAR_RESTAURANT = 2, ("Bar Restaurant")
        LOCAL_GUIDE = 3, ("Local Guide")
        EVENTS_AND_CONCERTS = 4, ("Events And Concerts")

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    identification_document = ESIdentityCardNumberField()
    typeClient = models.TextField(
        choices=TypeClient.choices, default=TypeClient.SMALL_BUSINESS
    )
    default_latitude = models.FloatField()
    default_longitude = models.FloatField()
    #subscription = models.ForeignKey(Subscription, related_name="Subscription", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OcialClientForm(ModelForm):
    class Meta:
        model = OcialClient
        fields = "__all__"


class OcialUserForm(ModelForm):
    class Meta:
        model = OcialUser
        fields = "__all__"
