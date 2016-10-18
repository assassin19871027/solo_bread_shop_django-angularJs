from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.db import models as normal_models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError
from urllib2 import URLError


LICENSE_TYPE = (
    (0, 'Commercial'),
    (1, 'cottage food operator / home operator'),
    (2, 'Not licensed'))


DELIVERY_METHOD = (
    (0, 'Delivery today'),
    (1, 'Delivery in future'),
    (2, 'Customer pickup'))


DELIVERY_SERVICE = (
    (0, 'Self'),
    (1, 'Postmates'),
    (2, 'Mailed'))


DELIVERY_FEE = (
    (0, 'Flat fee'),
    (1, 'Rate per mile radius'),
    (2, 'Min flat fee + rate per mile radius over min flat fee'),
    (3, 'None'))


class Baker(normal_models.Model):
    logo = models.ImageField(upload_to='bakers')
    business_name = models.CharField(max_length=100)
    business_owner_name = models.CharField(max_length=100)
    business_address = models.CharField(max_length=100)
    business_phone = models.CharField(max_length=20)
    business_cell_phone = models.CharField(max_length=20)
    business_email = models.EmailField()
    business_owner_email = models.EmailField()
    business_description = models.TextField()
    business_contact_name = models.CharField(max_length=100)

    license_type = models.IntegerField(choices=LICENSE_TYPE, default=2)
    license_expiration_date = models.DateTimeField()
    license_number = models.CharField(max_length=50, blank=True, null=True)

    began_at = models.DateTimeField()
    time_zone = normal_models.CharField(max_length=50, blank=True, null=True)

    url_pinterest = models.CharField(max_length=100, blank=True, null=True)
    url_instagram = models.CharField(max_length=100, blank=True, null=True)
    url_facebook = models.CharField(max_length=100, blank=True, null=True)
    url_twitter = models.CharField(max_length=100, blank=True, null=True)
    url_yelp = models.CharField(max_length=100, blank=True, null=True)
    url_business_website = models.CharField(max_length=100, blank=True, null=True)

    yelp_rating = models.FloatField(blank=True, null=True)
    yelp_comments = models.TextField(blank=True, null=True)

    customer_rating = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField()

    def __str__(self):
        return self.business_name

        
class Product(normal_models.Model):
    """
    Product model:
    Products are treated as blog posts. Seller can create multiple products, 
        each with own values for price, min unit, available dates, delivery method, etc.
    """
    baker = models.ForeignKey(Baker)
    # slug = models.SlugField(unique=True, max_length=10)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products')
    type = models.CharField(max_length=30)

    unit_price = normal_models.DecimalField(blank=True, null=False, default=00.00, 
                                            decimal_places=2, max_digits=6 ) # price in cents
    min_order_amount = normal_models.DecimalField(default=1.00, decimal_places=2, 
                                                  max_digits=6) # unit_price multiplied by min_order_unit 
    min_order_unit = normal_models.IntegerField(default=1)

    delivery_service = models.IntegerField(choices=DELIVERY_SERVICE, default=0)
    # delivery_service_provider = models.CharField(max_length=100)
    delivery_fee = models.IntegerField(choices=DELIVERY_FEE, default=0)
    delivery_method = models.IntegerField(choices=DELIVERY_METHOD, default=2)

    hashtags = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=500)
    order_fulfilment = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    num_views = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    num_shares = models.IntegerField(default=0)
    num_orders = models.IntegerField(default=0)

    customer_rating = models.FloatField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-date_created'] 
        
    def __str__(self):
        return '{}-{}'.format(self.baker.business_name, self.name)
        
    # def get_absolute_url(self):
    #     return reverse('products:view', kwargs={'slug': self.slug})


class BakerComment(normal_models.Model):
    baker = models.ForeignKey(Baker)
    created_at = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return self.baker.business_name


class ProductComment(normal_models.Model):
    product = models.ForeignKey(Product)
    created_at = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return self.product.name


class Sale(normal_models.Model):
    baker = models.ForeignKey(Baker)
    customer = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()
    traffic_source = models.CharField(max_length=100)
    first_visit_date = models.DateTimeField()
    visits_prior_checkout = models.IntegerField()
    avarage_time_on_pages = models.FloatField()
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    delivery_address = models.CharField(max_length=100)
    likes = models.TextField()
    shares = models.TextField()
    comments = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.baker.business_name, self.created_at)
