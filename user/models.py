from django.db import models
from django.contrib.auth.models import User
from localflavor.es.models import ESIdentityCardNumberField

class OcialUser(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.TextField()
    dni = ESIdentityCardNumberField(blank = True, null = True)
    '''
    La categoria esta en la rama de eventos
    fav_category = models.TextField(
        choices=Category.choices,
        default=Category.SPORTS
    )
    '''

    def __str__(self):
        return self.usuario.username

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new:
            city = self.city
            dni = self.dni