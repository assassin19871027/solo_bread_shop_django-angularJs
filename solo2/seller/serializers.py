from models import Product
from rest_framework import serializers


"""
ProductSerializer:
"""		
class ProductSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Product
		fields = ('url', 'photo', 'slug', 'caption')