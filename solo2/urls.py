from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from seller import views

"""
since we're using viewsets instead of views, we can automatically generate URL
conf for our API by registering the viewsets with out router class
"""
router = routers.SimpleRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'bakers', views.SellerViewSet)

""" 
wire up our API using automatic URL routing. Additionally, include login URLs for the browsable API.
"""
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    # url(r'^docs/', include('rest_framework_swagger.urls'))
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
