from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductList.as_view()),
    #  path("products/", views.product_list),
    path("products/<int:pk>/", views.ProductDetails.as_view()),
    #  path("products/<int:id>/", views.product_detail),
    path('collections/', views.CollectionList.as_view()),
    #  path('collections/', views.collection_list),
    path("collections/<int:pk>/", views.CollectionDetails.as_view(), name='collection-detail'),
    # path("collections/<int:pk>/", views.collection_details, name='collection-detail'),
]
