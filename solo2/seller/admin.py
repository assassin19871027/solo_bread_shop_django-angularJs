from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Baker)
admin.site.register(Product)
admin.site.register(BakerComment)
admin.site.register(ProductComment)
admin.site.register(Sale)