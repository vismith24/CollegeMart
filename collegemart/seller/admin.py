from django.contrib import admin
from .models import Category, Products_Selling
# Register your models here.
admin.site.register(Products_Selling)
admin.site.register(Category)
