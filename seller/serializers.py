from models import Product
from rest_framework import serializers


"""
ProductSerializer:
"""     
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # permission_classes = ['AllowAny',]
    baker_logo = serializers.SerializerMethodField(read_only=True)
    baker_name = serializers.SerializerMethodField(read_only=True)

    def get_baker_logo(self, obj):
    	return obj.baker.logo.url

    def get_baker_name(self, obj):
    	return obj.baker.business_name

    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'type', 'unit_price', 'min_order_amount', 'min_order_unit', 
                  'delivery_service', 'delivery_fee', 'delivery_method', 'hashtags', 'ingredients',
                  'order_fulfilment', 'description', 'num_views', 'num_shares', 'num_orders',
                  'num_likes', 'customer_rating', 'date_created', 'baker_logo', 'baker_name')
