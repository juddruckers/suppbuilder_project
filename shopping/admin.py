from django.contrib import admin

# Register your models here.

from .models import Address, Guest, Order

admin.site.register(Address)
admin.site.register(Guest)
admin.site.register(Order)