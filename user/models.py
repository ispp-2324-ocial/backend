from django.db import models
from django.contrib.auth.models import User
from localflavor.es.models import ESIdentityCardNumberField
from django.forms import ModelForm
from ocial.models import *
<<<<<<< HEAD

class OcialUser(models.Model):
    djangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    lastKnowLocLat = models.FloatField()
    lastKnowLocLong = models.FloatField()
    category = models.TextField(
        choices=[(category.value, category.name) for category in Category],
        default=Category.SPORTS.value,
    )
=======


class OcialUser(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_provider = models.TextField(
        choices=[(provider.value, provider.name) for provider in AuthProvider],
        default=AuthProvider.EMAIL.value,
    )
    lastKnowLocLat = models.FloatField()
    lastKnowLocLong = models.FloatField()

    def __str__(self):
        return self.djangoUser.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OcialClient(models.Model):
    djangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    identificationDocument = ESIdentityCardNumberField()
    typeClient = models.TextField(
        choices=[(typeclient.value, typeclient.name) for typeclient in TypeClient],
        default=TypeClient.SMALL_BUSINESS.value,
    )
    defaultLatitude = models.FloatField()
    defaultLongitude = models.FloatField()

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
