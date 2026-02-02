from django.shortcuts import render
from store.models import Product, OrderItem


# Create your views here.

def farm(request):
    queryset =  Product.objects.filter(
        id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    return render(request, "index.html", {"name": "Hassan", "products":list(queryset)})