from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class BakerAdmin(UserAdmin):
    fieldsets = None
    excludes = []

admin.site.register(Baker, BakerAdmin)
admin.site.register(Product)
admin.site.register(BakerComment)
admin.site.register(ProductComment)
admin.site.register(Sale)