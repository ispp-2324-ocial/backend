from django.contrib import admin


# Register your models here.

from .models import OcialUser, OcialClient

# Register your models here.
admin.site.register(OcialUser)
admin.site.register(OcialClient)