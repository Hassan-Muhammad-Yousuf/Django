from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    list_per_page = 5

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 5


admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)
