"""
This module provides comprehensive Django admin interface configuration for the store application,
enabling efficient management of Products, Customers, Orders, and Collections through the Django
admin panel.
CUSTOM FILTERS:
    InventoryFilter (admin.SimpleListFilter):
        A custom filter that allows filtering products by inventory levels.
        - Provides a 'low' option to display products with inventory less than 10 units
        - Inherits from SimpleListFilter for simple boolean-style filtering
        - Methods:
            * lookups(): Defines available filter options displayed in the admin interface
            * queryset(): Applies the selected filter logic to the queryset
ADMIN CLASSES:
    CustomerAdmin (admin.ModelAdmin):
        Manages Customer model display and editing in the admin interface.
        Configuration:
            - list_display: Shows first_name, last_name, membership status, and ordered products
            - list_editable: Allows inline editing of membership field directly from list view
            - list_per_page: Displays 5 customers per page for better performance
            - search_fields: Enables searching by first_name or last_name (case-insensitive prefix match)
        Optimizations:
            - get_queryset(): Uses prefetch_related() to fetch related Order and OrderItem objects
              with their Product data, reducing N+1 query problems
        Custom Methods:
            - ordered_products(): Displays all unique products ordered by each customer as a 
              comma-separated list. Uses set() to eliminate duplicates.
    ProductAdmin (admin.ModelAdmin):
        Manages Product model display, editing, and bulk operations.
        Configuration:
            - search_fields: Enables full-text search by product title
            - autocomplete_fields: Provides autocomplete dropdown for collection foreign key selection
            - prepopulated_fields: Auto-generates URL-friendly slug from title field
            - exclude: Hides 'promotions' field from the admin form
            - list_display: Shows title, unit_price, inventory_status, and collection information
            - list_editable: Allows inline editing of unit_price directly from list view
            - list_filter: Enables filtering by collection, last_updates date, and custom InventoryFilter
            - list_per_page: Displays 5 products per page
            - list_select_related: Uses select_related('collection') to optimize database queries by
              reducing queries for fetching related Collection objects
        Custom Actions:
            - clear_inventory(): Bulk action that sets inventory to 0 for selected products
              Displays error-level message confirming number of updated products
        Custom Display Methods:
            - collection_title(): Shows the title of the related collection for each product
            - inventory_status(): Returns 'Low' if inventory < 50, otherwise returns 'Ok'
              Uses @admin.display(ordering='inventory') to make this column sortable
    OrderItemInline (admin.TabularInline):
        Allows inline editing of OrderItem objects within the Order admin interface.
        Configuration:
            - model: Links to the OrderItem model for inline editing
            - min_num: Requires at least 1 OrderItem per Order
            - max_num: Limits maximum of 100 OrderItems per Order
            - autocomplete_fields: Provides autocomplete for product selection
            - extra: Displays 0 empty rows by default (only shows existing items)
        Purpose: Enables creation and editing of order items directly within the order form
                 without navigating to a separate OrderItem admin page
    OrderAdmin (admin.ModelAdmin):
        Manages Order model display and editing.
        Configuration:
            - list_display: Shows order ID, associated customer, placement date, and payment status
            - list_editable: Allows inline editing of payment_status directly from list view
            - autocomplete_fields: Provides autocomplete dropdown for customer foreign key selection
            - inlines: Embeds OrderItemInline for managing order items within the order form
        Purpose: Provides complete order management with ability to edit payment status and
                 manage related order items in one interface
    CollectionAdmin (admin.ModelAdmin):
        Manages Collection model display with product count annotation.
        Configuration:
            - list_display: Shows collection title and product count with clickable link
            - search_fields: Enables searching by collection title
        Optimizations:
            - get_queryset(): Annotates the queryset with Count('product') to efficiently
              count related products without additional queries
        Custom Display Methods:
            - products_count(): Returns a clickable hyperlink to the product changelist
              filtered by the current collection. Uses:
              * reverse(): Generates the URL for the product admin changelist
              * urlencode(): Encodes filter parameters as URL query string
              * format_html(): Creates safe HTML anchor tag with the generated URL
KEY FEATURES & BEST PRACTICES:
    Performance Optimization:
        - prefetch_related(): Used for reverse ForeignKey and ManyToMany relationships
                            Reduces queries by fetching related objects in separate calls
        - select_related(): Used for forward ForeignKey relationships
                          Joins related data in a single query
        - annotations with Count(): Computes aggregate statistics efficiently at database level
    User Experience:
        - list_editable: Allows quick inline editing of common fields without form navigation
        - autocomplete_fields: Provides efficient selection for foreign keys with large datasets
        - prepopulated_fields: Auto-generates slug from title, reducing manual data entry
        - Custom list filters: Simplifies data filtering and navigation
        - Search fields: Enables quick data discovery
    Data Integrity:
        - Custom actions with confirmation: Bulk operations like clear_inventory include
          user feedback via message_user()
        - Inline constraints (min_num, max_num): Ensures valid related object counts
        - Hyperlinked displays: Enables cross-filtering and related data inspection
    Admin Interface Enhancement:
        - Custom display methods with @admin.display decorators provide:
          * Sortable columns (ordering parameter)
          * HTML formatting capabilities (format_html)
          * Readable labels for computed fields

Django Admin Configuration for Store Application
This module configures the Django admin interface for managing store models including
Products, Customers, Orders, and Collections. It provides custom admin classes with
enhanced functionality for filtering, searching, displaying related data, and performing
bulk actions.
Key Components:
    - InventoryFilter: Custom filter for products based on inventory levels
    - CustomerAdmin: Admin interface for Customer model with order history display
    - ProductAdmin: Admin interface for Product model with inventory status and bulk actions
    - OrderItemInline: Inline editing for OrderItems within Order admin
    - OrderAdmin: Admin interface for Order model with payment status management
    - CollectionAdmin: Admin interface for Collection model with product count annotation
Features:
    - Custom list filters and search fields for efficient data lookup
    - Prefetch and select_related optimizations to reduce database queries
    - Inline editing of related objects
    - Custom actions for bulk operations (e.g., clearing inventory)
    - Formatted hyperlinks in list display for better navigation
    - Autocomplete fields for foreign key relationships
    - Query optimization using annotations and prefetching
"""


from django.contrib import admin, messages  # Importing admin and messages modules from Django 
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
            products_count = Count('products')
        )

# admin.site.register(models.Product, ProductAdmin)

