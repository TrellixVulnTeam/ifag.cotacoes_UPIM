from django.core.management import call_command
from django.test import TestCase

from ifag.models import City, Indicator, Source, Quotation, History


class CalculateAvgTest(TestCase):
    """ Teste de QuotationSearch """
    fixtures = [
        'city',
        'category',
        'unit',
        'group',
        'indicator',
        'source',
        'sourceindicatorcity',
        'quotation',
        'users',
    ]

    def setUp(self):
        """
        Configuração do teste
        """
        self.jatai = City.objects.get(name_ascii="JATAI")
        self.rioverde = City.objects.get(name_ascii="RIO VERDE")
        self.soja_disponivel = Indicator.objects.get(slug='soja-disponivel')
        self.soja_balcao = Indicator.objects.get(slug='soja-balcao')

    def test_aproved_2017_09_01(self):
        """
        Verifica se calcula as médias, se atualiza as cotações, se
        permite chamar novamente o comando sem mudar os resultados anteriores
        """

        "Cotações que precisam ser calculadas"
        queryset = Quotation.objects.filter(
            date='2017-09-01',
            status=Quotation.STATUS_APPROVED,
            calculated=False
        )
        self.assertEqual(queryset.count(), 4)

        "Se existe histórico calculado"
        queryset = History.objects.filter(date='2017-09-01')
        self.assertEqual(queryset.count(), 0)

        "Executa comando de calculo 2x"
        call_command("calculateavg")  # Calcula todas as cotações pendentes
        call_command("calculateavg")  # Chamar 2x não deve alterar o resultado

        "Se existe histórico calculado"
        queryset = History.objects.filter(date='2017-09-01')
        self.assertEqual(queryset.count(), 3)

        "Cotações que precisam ser calculadas"
        queryset = Quotation.objects.filter(
            date='2017-09-01',
            status=Quotation.STATUS_APPROVED,
            calculated=False
        )
        self.assertEqual(queryset.count(), 0)

    def test_update_history(self):
        """
        Verificando se é possível atualizar um histórico ao aprovar novas
        cotações
        """
        search_values = {
            'date': '2017-09-02',
            'city': City.objects.get(name_ascii="JATAI"),
            'indicator': Indicator.objects.get(slug='soja-disponivel')
        }

        " Calcula todas as cotações pendentes "
        call_command("calculateavg")
        instance = History.objects.get(**search_values)
        self.assertEqual(instance.value, 52.000)

        " Muda cotação para aprovada"
        quotation = Quotation.objects.get(
            source=Source.objects.get(name="João das Couves"),
            **search_values
        )
        quotation.status = Quotation.STATUS_APPROVED
        quotation.save()

        " Calcula as cotações novamente e verifica se o valor mudou "
        call_command("calculateavg")
        instance = History.objects.get(**search_values)
        self.assertEqual(instance.value, 54.000)
