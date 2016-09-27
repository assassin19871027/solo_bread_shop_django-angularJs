# Create your models here.
from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.db import models as normal_models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError
from urllib2 import URLError


class Baker(normal_models.Model):
    logo = models.ImageField()
    thumb = models.ImageField()
    business_name = models.CharField(max_length=100)
    business_owner_name = models.CharField(max_length=100)
    business_address = models.CharField(max_length=100)
    business_phone = models.IntegerField()
    business_cell_phone = models.CharField(max_length=20)
    business_email = models.EmailField()
    business_owner_email = models.EmailField()
    business_description = models.TextField()
    business_contact_name = models.CharField(max_length=100)
    permit_type = models.CharField(max_length=50)
    permit_expiration_date = models.DateTimeField()
    permit_number = models.IntegerField()
    delivery_method = models.CharField(max_length=100)
    delivery_service_provider = models.CharField(max_length=100)
    began_at = models.DateTimeField()
    time_zone = normal_models.CharField(max_length=50, blank=True, null=True)

    url_pinterest = models.CharField(max_length=100)
    url_instagram = models.CharField(max_length=100)
    url_facebook = models.CharField(max_length=100)
    url_twitter = models.CharField(max_length=100)
    url_yelp = models.CharField(max_length=100)
    url_business_website = models.CharField(max_length=100)

    yelp_rating = models.FloatField()
    yelp_comments = models.TextField()

    customer_rating = models.FloatField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.business_name

        
"""
Product model:
Products are treated as blog posts. Seller can create multiple products, each with own values for price, min unit, available dates, delivery method, etc.
"""
def generate_id():
    n = 10
    random = str.ascii_uppercase + str.ascii_lowercase + str.digits
    return ''.join(choice(random) for _ in range(n))

# products for each seller as a post element
class Product(normal_models.Model):
    baker = models.ForeignKey(Baker)
    slug = models.SlugField(unique=True, max_length=10, default=generate_id)
    name = models.CharField(max_length=100)
    image = models.ImageField()
    type = models.CharField(max_length=30)
    unit_price = normal_models.DecimalField(blank=True, null=False, default=00.00, decimal_places=2, max_digits=6 ) # price in cents
    min_order_amount = normal_models.DecimalField(default=1.00, decimal_places=2, max_digits=6) # unit_price multiplied by min_order_amount 
    min_order_unit = normal_models.IntegerField(default=1)
    photo = models.FileField()
    delivery_method = models.CharField(max_length=100)
    delivery_service = models.CharField(max_length=100)
    delivery_fee = models.FloatField()
    hashtags = models.CharField(max_length=50)

    ingredients = models.CharField(max_length=500)
    description = models.TextField()
    num_views = models.IntegerField()
    num_likes = models.IntegerField()
    num_shares = models.IntegerField()
    num_orders = models.IntegerField()
    customer_rating = models.FloatField()
    fulfilment_time = models.CharField(max_length=100)
    caption = models.CharField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-date_created'] 
        
    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('products:view', kwargs={'slug': self.slug})


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
