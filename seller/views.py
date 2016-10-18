from django.shortcuts import render

from models import Product, Baker
from rest_framework import viewsets
from serializers import ProductSerializer, SellerSerializer


class ProductViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows products to viewed or edited.
	"""
	queryset = Product.objects.all().order_by('-date_created')
	serializer_class = ProductSerializer


class SellerViewSet(viewsets.ModelViewSet):
	"""
	API endpoint for sellers
	"""
	queryset = Baker.objects.all()
	serializer_class = SellerSerializer
