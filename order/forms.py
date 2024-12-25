from django import forms

from order.models import Order, Shop


class AddOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['shop', ]

    shop = forms.ModelChoiceField(queryset=Shop.objects.none(), empty_label='Not specified', label='Shops')

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')
        super(AddOrderForm, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = user.shops.all()
