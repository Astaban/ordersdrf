from django import forms

from order.models import Order, Shop, OrderItem, Product


class AddOrderForm(forms.Form):
    def __init__(self, shops, products, *args, **kwargs):
        self.shops = forms.ModelChoiceField(queryset=shops)
        for product in products:
            setattr(self, product, forms.FloatField(label='Quantity', min_value=0.5))
        super().__init__(self, *args, **kwargs)

    class Meta:
        fields = '__all__'


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
