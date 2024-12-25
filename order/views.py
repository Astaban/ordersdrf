from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from rest_framework.generics import ListAPIView

from order.models import Product
from order.serializers import ProductSerializer


class MainPage(TemplateView):
    template_name = 'ordertemplates/main.html'


class ProductsList(LoginRequiredMixin, ListView):
    template_name = 'ordertemplates/products_list.html'
    context_object_name = 'products'
    allow_empty = True

    def get_queryset(self):
        products = Product.objects.all()
        return products


class ProductsListAPI(LoginRequiredMixin, ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
