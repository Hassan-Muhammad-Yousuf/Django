from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem

# Register your models here.
class TagInLine(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]
    

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)


"""
Django Admin Customization for Product Model with Tags

This module demonstrates:
1. GenericTabularInline - for displaying related objects via GenericForeignKey
2. Admin class inheritance - extending existing ProductAdmin
3. Inline editing - embedding TaggedItem forms within Product admin
4. Autocomplete fields - enabling search functionality for related objects

References:
- Django GenericRelations: https://docs.djangoproject.com/en/stable/contenttypes/
- Admin Inlines: https://docs.djangoproject.com/en/stable/ref/contrib/admin/#inlinemodelladu
- Registering Models: https://docs.djangoproject.com/en/stable/ref/contrib/admin/#the-register-decorator

Key Concepts:
- TaggedItem uses ContentType to create a generic relationship to any model
- CustomProductAdmin extends ProductAdmin and adds tag editing capability
- unregister/register allows overriding default admin configurations
"""