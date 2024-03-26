from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField()
    blurhash = models.TextField()
