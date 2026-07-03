from django.contrib import admin
from .models import Customer,Category,Products
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Products)