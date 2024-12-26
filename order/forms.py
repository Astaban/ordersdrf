from django import forms

from order.models import Order, Shop, OrderItem, Product


class AddOrderForm(forms.Form):
    def __init__(self, shops, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shops'] = forms.ModelChoiceField(queryset=shops, label='Магазин:', empty_label='Не выбрано.')
        for product in products:
            self.fields[product] = forms.FloatField(label=product, min_value=0.5, required=False)


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', ]

    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Product')
    quantity = forms.FloatField(min_value=0.5, label='Quantity')


class MyClass:

    def __init__(self, array):
        for attr in array:
            self.__setattr__(attr, 25)
