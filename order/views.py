from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from rest_framework.generics import ListAPIView

from order.forms import AddOrderForm
from order.models import Product, Order
from order.serializers import ProductSerializer


class MainPage(TemplateView):
    template_name = 'ordertemplates/main.html'


class AddOrder(LoginRequiredMixin, CreateView):

    model = Order
    form_class = AddOrderForm
    template_name = 'ordertemplates/add_order.html'
    success_url = reverse_lazy('main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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
