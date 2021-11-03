from django.core.management import BaseCommand
from django.db.models import Avg

from ifag.models import Quotation, History


class Command(BaseCommand):
    help = 'Calcula a média das cotações aprovadas'

    def handle(self, *args, **options):
        """
        Atualizando histórico dos indices aprovados
        :param args:
        :param options:
        """

        " Distincção cotações aprovadas e não calculadas "
        queryset = Quotation.objects \
            .filter(status=Quotation.STATUS_APPROVED, calculated=False) \
            .order_by('date') \
            .distinct('indicator', 'city', 'date')

        for quote_row in queryset:
            self._update_history(quote_row)

        msg = "{} histórico(s) atualizado(s)".format(queryset.count())
        self.stdout.write(self.style.SUCCESS(msg))

    def _update_history(self, quote_row):
        """
        Calcula o histórico da cotação, levando em conta outros
        que já foram calculados para garantir que é possível atualizar
        um histórico
        :param quote_row:
        """

        " Filtra cotações do dia "
        search_values = {
            'date': quote_row.date,
            'city': quote_row.city,
            'indicator': quote_row.indicator
        }
        queryset = Quotation.objects.filter(
            status=Quotation.STATUS_APPROVED,
            **search_values
        )
        current_avg = queryset.aggregate(value_avg=Avg('value'))['value_avg']

        " Filtra o histórico do dia anterior para calcular variação "
        try:
            yesterday = History.objects.filter(
                date__lt=quote_row.date,
                city=quote_row.city,
                indicator=quote_row.indicator
            ).order_by('-date')[0]
            variation = (current_avg * 100 / float(yesterday.value)) - 100
        except IndexError:
            "Primeiro da série não tem variação"
            variation = 0

        " Cria ou atualiza histórico do dia "
        try:
            instance = History.objects.get(**search_values)
        except History.DoesNotExist:
            instance = History(**search_values)

        instance.value = current_avg
        instance.variation = variation
        instance.save()

        " Marca as cotações como atualizadas "
        queryset.update(calculated=True)

        " Marca para recalcular as cotações mais novas se houver "
        Quotation.objects.filter(
            date__gt=quote_row.date,
            city=quote_row.city,
            indicator=quote_row.indicator
        ).update(calculated=False)
