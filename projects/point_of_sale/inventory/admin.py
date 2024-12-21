from django.contrib import admin
from .models import Product, Category, UnitType

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UnitType)
