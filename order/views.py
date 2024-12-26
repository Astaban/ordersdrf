from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from rest_framework.generics import ListAPIView

from order.forms import AddOrderForm, OrderItemForm
from order.models import Product, Order, OrderItem, Shop
from order.serializers import ProductSerializer


class MainPage(TemplateView):
    template_name = 'ordertemplates/main.html'


def add_order(request):

    shops = request.user.shops.all()
    products = [product.name for product in Product.objects.all()]
    # print(shops)
    # print(products)

    if request.method == 'POST':
        print('POST')
        form = AddOrderForm(shops=shops, products=products, data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            order = Order(shop=form.cleaned_data.pop('shops'))
            order.save()
            for product, quantity in form.cleaned_data.items():
                if quantity:
                    product_obj = Product.objects.get(name=product)
                    order_item = OrderItem(order=order, product=product_obj, quantity=quantity)
                    order_item.save()
            return HttpResponse(f'Заказ {order} сформирован.\n{order.show_order()}')
        else:
            return HttpResponse('Что-то пошло не так.')
    else:
        print('GET')
        form = AddOrderForm(shops=shops, products=products)
        return render(request, 'ordertemplates/add_order.html', {'form': form})


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
