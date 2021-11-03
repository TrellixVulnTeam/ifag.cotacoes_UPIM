from django.db.models import Min, Max, Avg
from rest_framework import viewsets, mixins, exceptions
from rest_framework.response import Response

from . import serializers
from .. import models


class CityList(mixins.ListModelMixin,
               viewsets.GenericViewSet):
    queryset = models.City.objects.get_has_indicator()
    serializer_class = serializers.CitySerializer

    def filter_queryset(self, queryset):
        """
        Filtrando as cidades desejadas desejados

        :param queryset:
        :return:
        """

        " Seleciona os filtros desejados "
        filters = {}
        if self.request.GET.get('indicator'):
            indicators = self.request.GET.get('indicator').split(',')
            filters = {
                'history__indicator__slug__in': indicators
            }

        qs = queryset.filter(**filters).distinct()
        return qs


class HistoryMashupList(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = models.History.objects.all()
    serializer_class = serializers.HistoryMashupSerializer

    def filter_queryset(self, queryset):
        """
        Filtrando os historicos desejados

        :param queryset:
        :return:
        """

        " Seleciona os filtros desejados "
        filters = {}
        search_keys = {
            'date': 'date',
            'city': 'city__pk',
            'indicator': 'indicator__slug__in',
        }
        for item, lookup in search_keys.items():
            value = self.request.GET.get(item)
            if value and '__in' in lookup:
                value = value.split(',')

            if value:
                filters[lookup] = value

        " Se nenhum filtro foi definido "
        if len(filters) == 0:
            raise exceptions.ValidationError(
                'É obrigatório fornecer algum parametro'
            )

        qs = queryset.filter(**filters) \
            .values('indicator', 'date') \
            .annotate(
            higher_avg=Max('value'),
            lower_avg=Min('value'),
            variation=Avg('variation'),
            avg=Avg('value')
        )

        result = []
        for item in qs:
            higher = queryset.filter(
                **filters,
                value=item['higher_avg'],
                indicator__pk=item['indicator']
            ).first()
            lower = queryset.filter(
                **filters,
                value=item['lower_avg'],
                indicator__pk=item['indicator']
            ).first()
            item.update({'lower_avg_city': lower.city})
            item.update({'higher_avg_city': higher.city})
            item.update({'indicator': higher.indicator})
            result.append(item)

        return result


class PublicationList(viewsets.ViewSet):
    def list(self, request):
        queryset = models.Publication.objects.aggregate(date=Max('date'))
        serializer = serializers.PublicationSerializer(
            instance=queryset,
            many=False
        )
        return Response(serializer.data)


class QuotationList(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Quotation.objects.all()
    serializer_class = serializers.QuotationSerializer

    def filter_queryset(self, queryset):
        """
        Filtrando as cotações desejadas

        :param queryset:
        :return:
        """

        " Seleciona os filtros desejados "
        filters = {}
        search_keys = {
            'date': 'date',
            'city': 'city__pk',
            'indicator': 'indicator__slug__in',
        }
        for item, lookup in search_keys.items():
            value = self.request.GET.get(item)
            if value and '__in' in lookup:
                value = value.split(',')

            if value:
                filters[lookup] = value

        " Se nenhum filtro foi definido "
        if len(filters) == 0:
            raise exceptions.ValidationError(
                'É obrigatório fornecer algum parametro: %s' %
                ', '.join(search_keys.keys())
            )
        return queryset.filter(**filters)
