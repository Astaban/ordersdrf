from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from rest_framework.generics import ListAPIView

from order.forms import AddOrderForm, OrderItemForm
from order.models import Product, Order, OrderItem, Shop
from order.serializers import ProductSerializer


class MainPage(TemplateView):
    template_name = 'ordertemplates/main.html'


class AddOrder(LoginRequiredMixin, CreateView):

    model = Order
    template_name = 'ordertemplates/add_order.html'
    success_url = reverse_lazy('main')
    shops = Shop.objects.all()
    products = [obj.name for obj in Product.objects.all()]
    form = AddOrderForm(shops, products)

    extra_context = {'form': form}
    def form_valid(self, form):
        order = form.save(commit=False)


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
