from django.contrib import admin


# Register your models here.

from .models import Event, Rating

# Register your models here.
admin.site.register(Event)
admin.site.register(Rating)