from django.db import models
from user.models import User


class Product(models.Model):

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    class Category(models.IntegerChoices):
        vegetable = 1, 'Овощи'
        fruit = 2, 'Фрукты'
        greens = 3, 'Зелень'
        dried = 4, 'Сухофрукты'
        other = 5, 'Прочее'

    class Unit(models.IntegerChoices):
        kg = 1, 'килограмм'
        box = 2, 'коробка/ящик'
        bag = 3, 'мешок/пакет'

    name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='Описание')
    category = models.IntegerField(choices=Category, verbose_name='Категория')
    unit = models.IntegerField(choices=Unit, verbose_name='Единица измерения')

    def __str__(self):
        return self.name


class Shop(models.Model):

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    short_name = models.CharField(max_length=8, verbose_name='Краткое наименование')
    full_name = models.CharField(max_length=100, verbose_name='Полное наименование')
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Адрес')
    vendors = models.ManyToManyField(User, related_name='shops', verbose_name='Продавцы')
    routing = models.ForeignKey('Routing', on_delete=models.CASCADE, null=True, blank=True, related_name='shops', verbose_name='Маршрут')
    routing_priority = models.PositiveIntegerField(blank=True, null=True, verbose_name='Порядок')

    def __str__(self):
        return self.full_name


class Routing(models.Model):

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    name = models.CharField(max_length=100, verbose_name='Маршрут')

    def __str__(self):
        return self.name

    def show_shops(self):
        shops = ', '.join([f'{item.full_name} {item.address}' for item in self.shops.all()])
        return shops


class Order(models.Model):

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(auto_now_add=True, verbose_name='Дата заказа')

    def __str__(self):
        return f'{self.shop.full_name} на {self.order_date}.'

    def show_order(self):
        order = self.items.all()
        details = ', '.join([f'{item.product.name} x {item.quantity}' for item in order])
        return details


class OrderItem(models.Model):

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
