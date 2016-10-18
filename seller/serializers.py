from models import Product, Baker
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
    ProductSerializer:
    """     
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


class SellerSerializer(serializers.HyperlinkedModelSerializer):
    """
    SellerSerializer or BakerSerializer:
    """     
    # permission_classes = ['AllowAny',]
    products = ProductSerializer(source='product_set', many=True, read_only=True)

    class Meta:
        model = Baker
        fields = ('id', 'logo', 'business_name', 'license_number', 'business_description', 'business_phone', 
                  'business_email', 'products')
