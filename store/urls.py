from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')



urlpatterns = router.urls + products_router.urls

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
