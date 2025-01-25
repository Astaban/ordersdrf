from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from order.forms import AddOrderForm
from order.models import Product, Order, OrderItem, Shop
from order.serializers import ProductSerializer


class MainPage(TemplateView):
    template_name = 'ordertemplates/main.html'


@login_required
def add_order(request):

    shops = request.user.shops.all()
    products_queryset = Product.objects.all()
    products = [product.name for product in products_queryset]

    print(f'{add_order.__name__} data setup start')
    print(shops)
    print(products)
    print(products_queryset)
    print(f'{add_order.__name__} data setup finish')

    if request.method == 'POST':
        print('POST')
        form = AddOrderForm(shops=shops, products=products, data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            order = Order(shop=form.cleaned_data.pop('shops'))
            order.save()
            for product, quantity in form.cleaned_data.items():
                if quantity:
                    product_obj = products_queryset.get(name=product)
                    order_item = OrderItem(order=order, product=product_obj, quantity=quantity)
                    order_item.save()
            return HttpResponse(f'Заказ {order} сформирован.\n{order.show_order()}')
        else:
            return HttpResponse('Что-то пошло не так.')
    else:
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


class ProductsListAPI(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Как все сложно без специализированных классов представлений

# class ProductsListAPI(LoginRequiredMixin, ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductsListAPI(APIView):
#
#     def get(self, request):
#         products = Product.objects.all()
#         return Response({'products': ProductSerializer(products, many=True).data})
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'product': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Product.objects.get(pk=pk)
#         except:
#             return Response({"error": "Such product does not exists"})
#
#         serializer = ProductSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"changes": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             instance = Product.objects.get(pk=pk)
#         except:
#             return Response({"error": "Such product does not exists"})
#
#         instance.delete()

    # def post(self, request):
    #     new_product = Product.objects.create(
    #         name=request.data.get('name'),
    #         description=request.data.get('description'),
    #         category=request.data.get('category'),
    #         unit=request.data.get('unit'),
    #     )
    #     return Response({'product': model_to_dict(new_product)})
