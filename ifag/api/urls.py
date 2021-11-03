from django.conf.urls import url, include
from rest_framework import routers

from . import views

# Rotas do django rest framework
router = routers.DefaultRouter()
router.register(r'cities', views.CityList, )
router.register(r'historymashup', views.HistoryMashupList, 'historymashup')
router.register(r'publication', views.PublicationList, 'publication')
router.register(r'quotation', views.QuotationList, 'quotation')

# Adicionado o Router as urls do django
urlpatterns = [
    url(r'^', include(router.urls)),
]
