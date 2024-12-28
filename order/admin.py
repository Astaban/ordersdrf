from functools import wraps

from django.contrib import admin
from django.shortcuts import render

from order import models
from django.utils import timezone
from time import time

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
    def generate_invoice(orders):
        invoice = {}
        if isinstance(orders, models.Order):
            items = orders.items.all()
            for item in items:
                invoice.update({item.product.name: item.quantity})
            return invoice
        else:
            for order in orders:
                for item in order.items.all():
                    if item.product.name in invoice.keys():
                        invoice[item.product.name] += item.quantity
                    else:
                        invoice[item.product.name] = item.quantity
            return invoice

    @admin.action(description='Все заказали?')
    def check_orders(self, request, queryset):
        today = timezone.now().date()
        queryset = models.Order.objects.filter(order_date=today)
        self.message_user(request, f'Заказали {queryset.count()} из {models.Shop.objects.count()} магазинов.')

    @admin.action(description='Формировать заказ')
    @duration_time_measurer
    def finalize_order(self, request, queryset):
        invoices = []
        today = timezone.now().date()
        today_orders = models.Order.objects.filter(order_date=today)
        routings = models.Routing.objects.all()

        print('data created')

        full_invoice = {'name': 'Общий заказ:'}
        full_invoice.update(self.generate_invoice(today_orders))
        invoices.append(full_invoice)

        print('full_invoice created')

        for routing in routings:
            routing_invoice = {'name': f'{routing.name}:'}
            shops = routing.shops.all()
            orders = today_orders.filter(shop__in=shops)
            routing_invoice.update(self.generate_invoice(orders))
            invoices.append(routing_invoice)

        print('routings_invoices created')

        for order in today_orders:
            shop_invoice = {'name': f'{order.shop}:'}
            shop_invoice.update(self.generate_invoice(order))
            invoices.append(shop_invoice)

        print('shops_invoices created')

        [print(invoice) for invoice in invoices]
        return render(request, 'ordertemplates/invoice_table.html', {'invoice_data': invoices})

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


