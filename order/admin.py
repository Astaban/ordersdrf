from functools import wraps

from django.contrib import admin
from django.shortcuts import render

from order import models
from django.utils import timezone
from time import time

import pandas as pd

from order.models import Shop

admin.site.site_header = "Панель Администратора"
admin.site.index_title = "Заказы. Магазины. Товары"


def duration_time_measurer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        stop = time()
        duration = stop - start
        print(f'{func.__name__} duration time: {round(duration, 2)}')
        return result
    return wrapper


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'unit', )
    list_display_links = ('name', )
    list_editable = ('category', 'unit', )
    search_fields = ('name__contains', )
    ordering = ('category', 'name', )
    list_filter = ('category', )
    list_per_page = 100
    save_on_top = True


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'routing', 'routing_priority')
    list_display_links = ('full_name', )
    search_fields = ('full_name__contains', )
    list_editable = ('routing', 'routing_priority', )
    ordering = ('routing', 'routing_priority', 'full_name', )
    list_filter = ('routing', )
    filter_horizontal = ('vendors', )
    list_per_page = 25
    save_on_top = True


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = [OrderItemInline]
    actions = ('check_orders', 'finalize_order', )
    ordering = ('order_date', 'shop__full_name', )
    list_filter = ('order_date', )

    @staticmethod
    def process_orders_to_products_list(orders):
        """Создает сортированный список уникальных названий всех товаров, содержащихся в
        queryset orders; для ограничения нагрузки на БД желательно использовать select_related('product')
        при формировании queryset orders до его передачи методу"""
        product_names = set()
        for order in orders:
            order_products_names = {item.product.name for item in order.items.all().select_related('product')}
            product_names = product_names.union(order_products_names)
        product_names = sorted(product_names)
        return product_names

    @staticmethod
    def process_order_to_dict(order, product_names):
        """Создает словарь для дальнейшего использования в создании датафрейма;
        product_names - список строковых значений - названий товаров (обязательно сортирован);
        order - объект Order;
        возвращает словарь, ключ которого - краткое название магазина,
        значения - список, элементы которого - количество товаров, входящих в product_names,
        которые заказаны в заказе order (если их нет в заказе - добавляется значение 0)"""
        column_values = []
        order_dict = {order.shop.short_name: column_values}
        order_items = order.items.all()
        for product in product_names:
            if order_items.filter(product__name=product).exists():
                order_item = order.items.get(product__name=product)
                column_values.append(order_item.quantity)
            else:
                column_values.append(0)
        # print(product_names)
        # print(order_dict)
        return order_dict

    def process_orders_to_dataframe(self, orders, product_names):
        """Создает датафрейм для представления накладной, маршрута, общей накладной;
        product_names - список строковых значений - названий товаров (обязательно сортирован);
        orders - queryset объектов Order;
        возвращает pandas dataframe, в котором строки - наименования товаров, столбцы - наименования магазинов,
        ячейки - количество конкретного товара, заказанного на конкретный магазин"""
        tb_data = {}
        for order in orders:
            tb_data.update(self.process_order_to_dict(order, product_names))

        data_frame = pd.DataFrame(tb_data, index=list(product_names))
        data_frame['Итого:'] = data_frame.sum(axis=1)
        return data_frame


    @admin.action(description='Все заказали?')
    def check_orders(self, request, queryset):
        today = timezone.now().date()
        queryset = models.Order.objects.filter(order_date=today)
        self.message_user(request, f'Заказали {queryset.count()} из {models.Shop.objects.count()} магазинов.')

    @admin.action(description='Формировать заказ')
    @duration_time_measurer
    def finalize_order(self, request, queryset):

        #------------------формируем и наполняем используемые структуры данных
        dataframes_set = {}
        today = timezone.now().date()
        today_orders = models.Order.objects.filter(order_date=today).select_related('shop')
        routings = models.Routing.objects.all()


        #------------------формируем общий заказ на все точки
        orders = today_orders
        product_names = self.process_orders_to_products_list(orders)
        data_frame = self.process_orders_to_dataframe(orders, product_names)
        dataframes_set.update({'Общий заказ': data_frame})

        #------------------формируем заказы на маршруты
        for routing in routings:
            orders = today_orders.filter(shop__routing=routing)
            product_names = self.process_orders_to_products_list(orders)
            data_frame = self.process_orders_to_dataframe(orders, product_names)
            dataframes_set.update({f'{routing.name}': data_frame})

        #------------------формируем заказы на магазины
        for shop in Shop.objects.all():
            orders = today_orders.filter(shop=shop)
            product_names = self.process_orders_to_products_list(orders)
            data_frame = self.process_orders_to_dataframe(orders, product_names)
            dataframes_set.update({f'{shop.name}': data_frame})

        for k, v in dataframes_set.items():
            print(k)
            print(v)
            print('*'*25)

        # return render(request, 'ordertemplates/invoice_table.html', {'invoice_data': invoices})

    def show_order(self, obj):
        return obj.show_order()
    show_order.short_description = 'Детали заказа'


class ShopsInline(admin.TabularInline):
    model = models.Shop
    extra = 0


@admin.register(models.Routing)
class RoutingAdmin(admin.ModelAdmin):

    inlines = [ShopsInline]

    def show_shops(self, obj):
        return obj.show_shops()
    show_shops.short_description = 'Детали маршрута'


# @admin.register(models.OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     pass


