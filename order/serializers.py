from rest_framework.serializers import ModelSerializer

from order.models import Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'category', 'unit')
