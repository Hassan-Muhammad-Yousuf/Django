from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html , urlencode
from django.urls import reverse
from . import models
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'low')
        ]
        
    def queryset(self, request, queryset):
        if self.value == '<10':
            return queryset.filter(inventory__lt = 10)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','ordered_products']
    list_editable = ['membership']
    list_per_page = 5
    search_fields = ['first_name__istartswith' , 'last_name__istartswith']
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'order_set__orderitem_set__product'
        )
    @admin.display(ordering='Ordered Products')   
    def ordered_products(self, obj):
        products = set()
        for order in obj.order_set.all():
            for item in order.orderitem_set.all():
                products.add(item.product.title)  # use product.title instead of name
        return ", ".join(products) if products else "-"


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    exclude = ['promotions']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_updates', InventoryFilter]
    list_per_page = 5
    list_select_related = ['collection']
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 50:
            return 'Low'
        return 'Ok'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count =queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    min_num = 1
    max_num = 100
    autocomplete_fields = ['product']
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'placed_at' ,'payment_status']
    list_editable = ['payment_status']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
            )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

# admin.site.register(models.Product, ProductAdmin)
