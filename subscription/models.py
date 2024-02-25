from django.db import models

class Subscription(models.Model):
    class TypeSubscription(models.TextChoices):
        FREE = 0, ('Free')
        BASIC = 1, ('Basic')
        PRO = 2, ('Pro')

    typeSubscription = models.TextField(
        choices = TypeSubscription.choices,
        default = TypeSubscription.FREE
    )
    numEvents = models.PositiveIntegerField(default=1)
    canEditEvent = models.BooleanField(default=False)
    canSendNotifications = models.BooleanField(default=False)
    canHaveRecurrentEvents = models.BooleanField(default=False)
    canHaveOustandingEvents = models.BooleanField(default=False)
    canHaveRating = models.BooleanField(default=False)


    def str(self):
        return "{}".format(self.typeSubscription)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            typeSubscription = self.typeSubscription