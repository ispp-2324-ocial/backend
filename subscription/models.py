from django.db import models
from django.forms import ModelForm
from user.models import OcialClient
from .models import *
from ocial.models import *


class Subscription(models.Model):

    typeSubscription = models.TextField(
        choices=[(type.value, type.name) for type in TypeSubscription],
        default=TypeSubscription.FREE.value,
    )
    numEvents = models.PositiveIntegerField(default=1)
    canEditEvent = models.BooleanField(default=False)
    canSendNotifications = models.BooleanField(default=False)
    canHaveRecurrentEvents = models.BooleanField(default=False)
    canHaveOustandingEvents = models.BooleanField(default=False)
    canHaveRating = models.BooleanField(default=False)
    ocialClientId = models.ForeignKey(
        OcialClient, related_name="OcialClientId", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.get_typeSubscription_display()} Subscription"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            self.typeSubscription
            self.numEvents
            self.canEditEvent
            self.canSendNotifications
            self.canHaveRecurrentEvents
            self.canHaveOustandingEvents
            self.canHaveRating
            self.ocialClientId


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"
