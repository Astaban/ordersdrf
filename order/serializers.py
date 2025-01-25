import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from order.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'unit')

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.save()
        return instance


# #######################Non-usable cod, just tests during education

# class TestClass:
#
#     def __init__(self, title, description):
#         self.title = title
#         self.description = description
#
# class TestClassSerializer(serializers.Serializer):
#
#     title = serializers.CharField(max_length=250)
#     description = serializers.CharField()


# def encode():
#     model = TestClass('title', 'description')
#     model_sr = TestClassSerializer(model)
#     print(model_sr.data, type(model_sr), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Title","description":"Description"}')
#     data = JSONParser().parse(stream)
#     deserialized_object = TestClassSerializer(data=data)
#     if deserialized_object.is_valid():
#         print(deserialized_object.validated_data)

