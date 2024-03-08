from django.db import models
from django.forms import ModelForm
from django import forms


class Subscription(models.Model):
    class TypeSubscription(models.TextChoices):
        FREE = 0, ("Free")
        BASIC = 1, ("Basic")
        PRO = 2, ("Pro")

    typeSubscription = models.TextField(
        choices=TypeSubscription.choices, default=TypeSubscription.FREE
    )
    numEvents = models.PositiveIntegerField(default=1)
    canEditEvent = models.BooleanField(default=False)
    canSendNotifications = models.BooleanField(default=False)
    canHaveRecurrentEvents = models.BooleanField(default=False)
    canHaveOustandingEvents = models.BooleanField(default=False)
    canHaveRating = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.typeSubscription)

    def save(self, *args, **kwargs):
        is_new = not self.pk

        if self.typeSubscription == self.TypeSubscription.FREE:
            self.numEvents = 1
        if self.typeSubscription == self.TypeSubscription.BASIC:
            self.numEvents = 10
            self.canHaveRating = True
            self.canEditEvent = True
        if self.typeSubscription == self.TypeSubscription.PRO:
            self.numEvents = None
            self.canHaveRating = True
            self.canEditEvent = True
            self.canHaveOustandingEvents = True
            self.canHaveRecurrentEvents = True
            self.canSendNotifications = True
        super().save(*args, **kwargs)

        if is_new:
            self.typeSubscription
            self.numEvents
            self.canEditEvent
            self.canSendNotifications
            self.canHaveRecurrentEvents
            self.canHaveOustandingEvents
            self.canHaveRating

class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"
        #fields = []
    """
    def clean(self):
        cleaned_data = super().clean()
        typeSubscription = cleaned_data.get('subscription_id')

        if typeSubscription:
            try:
                subcription_type = Subscription.TypeSubscription(int(typeSubscription))
            except ValueError:
                raise forms.ValidationError("Tipo de suscripción no válido")
            
            subscription = Subscription(typeSubscription=subcription_type)
            cleaned_data['subscription'] = subscription
        
        return cleaned_data
    """