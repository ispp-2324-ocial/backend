from django.contrib import admin


# Register your models here.

from .models import Event, Rating, Like

# Register your models here.
admin.site.register(Event)
admin.site.register(Rating)
admin.site.register(Like)
