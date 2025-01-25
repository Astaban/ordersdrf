from django.urls import path

from order import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('order/', views.add_order, name='order'),
    # path('order/', views.AddOrder.as_view(), name='order'),
    path('api/v1/order/', views.ProductsListAPI.as_view(), name='orderAPI_GET/POST'),
    path('api/v1/order/<int:pk>/', views.ProductsListAPI.as_view(), name='orderAPI_PUT'),

]
