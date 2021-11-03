from rest_framework import serializers

from .. import models


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ('pk', 'name', 'uf',)


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = ('pk', 'name',)


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Indicator
        fields = ('pk', 'name', 'unit', 'slug',)


class HistoryMashupSerializer(serializers.Serializer):
    indicator = IndicatorSerializer()
    lower_avg_city = CitySerializer()
    higher_avg_city = CitySerializer()
    lower_avg = serializers.DecimalField(7, 3, coerce_to_string=False)
    higher_avg = serializers.DecimalField(7, 3, coerce_to_string=False)
    avg = serializers.DecimalField(7, 3, coerce_to_string=False)
    date = serializers.DateField()
    variation = serializers.DecimalField(7, 3, coerce_to_string=False)


class PublicationSerializer(serializers.Serializer):
    date = serializers.DateField()


class QuotationSerializer(serializers.Serializer):
    date = serializers.DateField()
    indicator = IndicatorSerializer()
    source = SourceSerializer()
    city = CitySerializer()
    value = serializers.DecimalField(7, 3, coerce_to_string=False)
    status = serializers.CharField()
