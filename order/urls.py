from django.urls import path, include
from rest_framework import routers

from order import views
from order.views import ProductViewSet

product_router = routers.SimpleRouter()
product_router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('order/', views.add_order, name='order'),
    path('api/v1/', include(product_router.urls), name='productAPI_CRUD')
    # path('order/', views.AddOrder.as_view(), name='order'),
    # path('api/v1/products/', views.ProductsListAPI.as_view(), name='productsAPI_GET/POST'),
    # path('api/v1/product/<int:pk>/', views.ProductsUpdateAPI.as_view(), name='productsAPI_PUT'),
    # path('api/v1/product_detail/<int:pk>/', views.ProductsDetailAPI.as_view(), name='productsAPI_CRUD'),

]
