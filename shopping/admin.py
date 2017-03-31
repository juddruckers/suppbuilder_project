from django.contrib import admin

# Register your models here.

from .models import Address, Guest

admin.site.register(Address)
admin.site.register(Guest)