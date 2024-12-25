from django.urls import path

from order import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('order/', views.ProductsList.as_view(), name='order'),
    path('api/v1/order/', views.ProductsListAPI.as_view(), name='orderAPI'),

]
