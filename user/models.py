from django.db import models
from django.contrib.auth.models import User
from localflavor.es.models import ESIdentityCardNumberField
from django.forms import ModelForm
from ocial.models import *
from images.models import Image
from django.core.validators import MaxValueValidator, MinValueValidator


class OcialUser(models.Model):
    djangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
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
    image = models.ForeignKey(
        Image,
        related_name="ClientImage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Rating(models.Model):
    score = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    comment = models.TextField(blank=True, null=True)
    client = models.ForeignKey(OcialClient, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)

    def __str__(self):
        return f"Rating for {self.client}: {self.score} - {self.comment}"


class OcialClientForm(ModelForm):
    class Meta:
        model = OcialClient
        fields = "__all__"


class OcialUserForm(ModelForm):
    class Meta:
        model = OcialUser
        fields = "__all__"
