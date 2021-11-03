from django.conf.urls import url

from .views import QuotationInsert

urlpatterns = [
    url(
        r'^quotationinsert/$',
        QuotationInsert.as_view(),
        name='quotation_insert'
    ),
]
