from django.db import models
from django.contrib.auth.models import User
from localflavor.es.models import ESIdentityCardNumberField
from django.forms import ModelForm
from ocial.models import *


class OcialUser(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    lastKnowLocLat = models.FloatField()
    lastKnowLocLong = models.FloatField()
    category = models.TextField(
        choices=[(category.value, category.name) for category in Category],
        default=Category.SPORTS.value,
    )

    def __str__(self):
        return self.usuario.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OcialClient(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField()
    identification_document = ESIdentityCardNumberField()
    typeClient = models.TextField(
        choices=[(typeclient.value, typeclient.name) for typeclient in TypeClient],
        default=TypeClient.SMALL_BUSINESS.value,
    )
    default_latitude = models.FloatField()
    default_longitude = models.FloatField()

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
