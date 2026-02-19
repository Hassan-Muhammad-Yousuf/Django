from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)


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
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MTU5MjQ3MCwiaWF0IjoxNzcxNTA2MDcwLCJqdGkiOiI4YTEwMTEwNjUyNmY0ZjBjYmYxNTVlZWI1OTlkZTM3NCIsInVzZXJfaWQiOiIyIn0.CTnn9wfxSTW85Q-VifKk5cJlOaAfqPkO0mBDZ5Dpu6I",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcxNTkyNDcwLCJpYXQiOjE3NzE1MDYwNzAsImp0aSI6IjY4NDdhMDgyNmYwNDQ5ZWRhNWM3NTU5ZGVhMWQwNDhjIiwidXNlcl9pZCI6IjIifQ.h0xRsl1WUbxStuy8yP1LDnTOodXpJ8vzbhWGp18p29A"
# }