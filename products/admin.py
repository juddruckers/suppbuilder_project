from django.contrib import admin

# Register your models here.

from . models import Product, Variation, Research, Category, Benefit

admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(Research)
admin.site.register(Category)
admin.site.register(Benefit)
