from django.contrib import admin
from .models import Category, Products_Selling, Products_Leasing, commonNotification, Request_table
# Register your models here.
admin.site.register(Products_Selling)
admin.site.register(Category)
admin.site.register(Products_Leasing)
admin.site.register(commonNotification)
admin.site.register(Request_table)
