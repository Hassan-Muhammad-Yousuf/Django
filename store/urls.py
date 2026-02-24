from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')


products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename = 'cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls

# urlpatterns = [
#     path("products/", views.ProductList.as_view()),
#     #  path("products/", views.product_list),
#     path("products/<int:pk>/", views.ProductDetails.as_view()),
#     #  path("products/<int:id>/", views.product_detail),
#     path('collections/', views.CollectionList.as_view()),
#     #  path('collections/', views.collection_list),
#     path("collections/<int:pk>/", views.CollectionDetails.as_view(), name='collection-detail'),
#     # path("collections/<int:pk>/", views.collection_details, name='collection-detail'),
# ]





# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjAyMjM3MiwiaWF0IjoxNzcxOTM1OTcyLCJqdGkiOiIyNmY0MGU1NWNhMzc0OTM5ODY4ZDQwOWQ4ZWQzZmFhZSIsInVzZXJfaWQiOiIyIn0.qUCBfNO3UMuvnNhFCOJUSIesl-v6tqsE0quK2XSh_q0",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcyMDIyMzcyLCJpYXQiOjE3NzE5MzU5NzIsImp0aSI6ImQxZmU4YjFkZjE2NzRhNzdiMDQ0NmMzNDgwNmQ5YTE0IiwidXNlcl9pZCI6IjIifQ.Ylk7mEe9adm5EGA3CphWCHN1fHMtLI6CkA2xkxte-88"
# }