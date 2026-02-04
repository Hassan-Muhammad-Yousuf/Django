from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
# # The commented lines in the code are importing various modules and classes from Django's database
# models to perform operations on the database. Here is a breakdown of each import statement:
# from django.db.models.aggregates import Count,Max,Min,Avg
# from django.db.models import Value, F, Func, ExpressionWrapper, DecimalField
# # from django.db.models.functions import Concat
from store.models import Product, Customer
from tags.models import TaggedItem


# Create your views here.

def farm(request):
    
    TaggedItem.objects.get_tags_for(Product, 1)
    
    
    # content_type = ContentType.objects.get_for_model(Product)
    
    # quarry_set = TaggedItem.objects\
    # .select_related('tag')\
    #     .filter(
    #     content_type = content_type,
    #     object_id = 1
    # )
    
    
    # discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(
    #     discounted_price = discounted_price 
    # )
    # queryset = Customer.objects.annotate(
    #     orders_count = Count('order')
    # )
    # queryset = Customer.objects.annotate(
    #     full_name = Func(F('first_name'), Value(' '), F('last_name'), function= 'CONCAT')
    # )
    # queryset = Customer.objects.annotate(
    #     full_name= Concat('first_name', Value(' '), 'last_name')
    # )
    #queryset = Customer.objects.annotate(new_id = F('id') + 1)
    # result = Product.objects.filter(collection__id=1).aggregate(count = Count('id'), min_price = Min('unit_price'))
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # queryset =  Product.objects.prefetch_related('promotions').select_related('collection').all()
    
    return render(request, "index.html", {"name": "Hassan", 'tag' : list(quarry_set)})