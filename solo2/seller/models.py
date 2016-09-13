# Create your models here.
from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.db import models as normal_models
from django.conf import settings
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderQueryError
from urllib2 import URLError



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
	slug = models.SlugField(unique=True, max_length=10, default=generate_id)
	photo = models.FileField()
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

		



