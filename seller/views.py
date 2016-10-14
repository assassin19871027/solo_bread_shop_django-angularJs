from django.shortcuts import render

from models import Product
from rest_framework import viewsets
from serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows products to viewed or edited.
	"""
	queryset = Product.objects.all().order_by('-date_created')
	serializer_class = ProductSerializer