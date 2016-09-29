from models import Product
from rest_framework import serializers


"""
ProductSerializer:
"""     
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # permission_classes = ['AllowAny',]
    
    class Meta:
        model = Product
        fields = ('name', 'image', 'type', 'unit_price', 'min_order_amount', 'min_order_unit', 
                  'delivery_service', 'delivery_fee', 'delivery_method', 'hashtags', 'ingredients',
                  'order_fulfilment', 'description', 'num_views', 'num_shares', 'num_orders',
                  'num_likes', 'customer_rating', 'date_created')
