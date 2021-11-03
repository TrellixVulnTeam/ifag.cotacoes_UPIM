import json
from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ifag.forms import QuotationSearch
from ifag.models import Source, City, Indicator, Quotation


class QuotationSearchTest(TestCase):
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
    ]

    def setUp(self):
        """
        Configuração do teste
        """

        " Produtos "
        self.soja_disponivel = Indicator.objects.get(slug='soja-disponivel')
        self.soja_balcao = Indicator.objects.get(slug='soja-balcao')
        self.boi = Indicator.objects.get(slug='boi-gordo')

        " Cidades "
        self.mineiros = City.objects.get(name_ascii="MINEIROS")
        self.goiania = City.objects.get(name_ascii="GOIANIA")
        self.jatai = City.objects.get(name_ascii="JATAI")
        self.acreuna = City.objects.get(name_ascii="ACREUNA")

    def get_form(self, **kwargs):
        return QuotationSearch(**kwargs)

    def test_initial(self):
        form = self.get_form()
        self.assertFalse(form.is_valid())
        self.assertEqual(form.initial['date'], date.today())

    def test_city_none(self):
        form = self.get_form(data={'city': ''})
        self.assertFalse(form.is_valid())

    def test_category_none(self):
        form = self.get_form(data={'category': ''})
        self.assertFalse(form.is_valid())

    def test_indicators_none(self):
        form = self.get_form(data={'indicators': ''})
        self.assertFalse(form.is_valid())

    def test_ok(self):
        form = self.get_form(data={
            'date': date.today(),
            'category': 1,
            'city': self.jatai.pk,
            'indicators': [
                self.soja_disponivel.pk,
                self.soja_balcao.pk,
            ]
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_count_of_indicators(self):
        """
        Os parametros devem filtrar os indicadores disponíveis para seleção
        """
        " Sem categoria "
        form = self.get_form(data={
            'date': date.today(),
            'category': None,
            'city': self.goiania.pk
        })
        self.assertEqual(form.fields['indicators'].choices.queryset.count(), 3)

        " Sem cidade "
        form = self.get_form(data={
            'date': date.today(),
            'category': 2,
            'city': None
        })
        self.assertEqual(
            form.fields['indicators'].choices.queryset.count(),
            10
        )

        " Sem indicadores para os filtros "
        form = self.get_form(data={
            'date': date.today(),
            'category': 2,
            'city': self.acreuna.pk
        })
        self.assertEqual(form.fields['indicators'].choices.queryset.count(), 0)

        " Retorna opções disponíveis para os valores informados "
        form = self.get_form(data={
            'date': date.today(),
            'category': 2,
            'city': self.goiania.pk
        })
        self.assertEqual(form.fields['indicators'].choices.queryset.count(), 1)

        " Retorna opções disponíveis para os valores informados "
        form = self.get_form(data={
            'date': date.today(),
            'category': 1,
            'city': self.goiania.pk
        })
        self.assertEqual(form.fields['indicators'].choices.queryset.count(), 2)

    def test_queryset(self):
        instance = Quotation(**{
            "source": Source.objects.get(pk=1),
            "indicator": self.boi,
            "city": self.mineiros,
            "date": "2017-08-08",
            "value": 59.000
        })
        instance.save()

        form = self.get_form(data={
            'date': date(2017, 8, 8),
            'category': 2,
            'indicators': [self.boi.pk],
            "city": self.mineiros.pk,
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_queryset().count(), 1)


class QuotationInsertTest(TestCase):
    fixtures = [
        'city',
        'category',
        'unit',
        'group',
        'indicator',
        'source',
        'sourceindicatorcity',
        'users',
        'quotation',
    ]

    def setUp(self):
        """
        Configuração do teste
        """
        " Usuário "
        self.user = User.objects.get(username="diego")

        " Produtos "
        self.soja_balcao = Indicator.objects.get(slug='soja-balcao')
        self.soja_disponivel = Indicator.objects.get(slug='soja-disponivel')
        self.boi = Indicator.objects.get(slug='boi-gordo')

        " Cidades "
        self.jatai = City.objects.get(name_ascii="JATAI")
        self.palmeiras = City.objects.get(name_ascii="PALMEIRAS DE GOIAS")
        self.goiania = City.objects.get(name_ascii="GOIANIA")

        " Fontes "
        self.joao = Source.objects.get(name="João das Couves")
        self.cargil = Source.objects.get(name="Cargill")

    def _login(self):
        """ Realiza login. """
        self.client.force_login(self.user)

    def _get_url(self, **kwargs):
        """ Url da view """
        return reverse('ifag:quotation_insert', kwargs=kwargs)

    def test_not_logged(self):
        """ Redireciona para tela de login quando não logado. """
        response = self.client.get(self._get_url(), follow=True)
        redirect_url = reverse('admin:login')
        redirect_url += '?next=' + self._get_url()
        self.assertRedirects(response, redirect_url)

    def test_200(self):
        """ Testa se está tudo ok com view com GET. """
        self._login()
        response = self.client.get(self._get_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhuma fonte de informação encontrada")

    def test_200_full_filled(self):
        """ Testa se está tudo ok com view com GET. """
        self._login()

        " Agricultura / Palmeiras de Goias "
        data = {
            'date': date.today(),
            'category': 1,
            'city': self.palmeiras.pk,
        }
        response = self.client.get(self._get_url(), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Nenhuma fonte de informação encontrada"
        )

        " Pecuária / Goiânia / Boi Gordo Rastreado"
        data = {
            'date': date.today(),
            'category': 2,
            'city': self.goiania.pk,
            'indicators': [self.boi.pk]
        }

        response = self.client.get(self._get_url(), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            "Nenhuma fonte de informação encontrada"
        )

        " Agricultura / Jataí / Soja disponível e balcão"
        data = {
            'date': date.today(),
            'category': 1,
            'city': self.jatai.pk,
            'indicators': [self.soja_balcao.pk, self.soja_disponivel.pk]
        }

        response = self.client.get(self._get_url(), data)
        self.assertEqual(response.status_code, 200)

        # João das couves / BALCÃO / N/A
        self.assertContains(response, "N/A", 1)

        # João 1 / Cargil 2
        self.assertContains(response, '<input type="number"', 3)

        # SOJA DISPONÍVEL
        self.assertContains(response, self.joao.name, 1)

        # DISPONÍVEL / BALCÃO
        self.assertContains(response, self.cargil.name, 1)

        " Agricultura / Jataí / Balcão"
        data = {
            'date': date.today(),
            'category': 1,
            'city': self.jatai.pk,
            'indicators': [self.soja_balcao.pk]
        }

        response = self.client.get(self._get_url(), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "N/A")
        self.assertNotContains(response, "João das Couves")
        self.assertContains(response, '<input type="number"', 1)

        " Agricultura / Jataí / Disponível : Item rejeitado"
        data = {
            'date': '03/09/2017',
            'category': 1,
            'city': self.jatai.pk,
            'indicators': [self.soja_disponivel.pk]
        }

        response = self.client.get(self._get_url(), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rejeitada')

    def test_post_status(self):
        """
        Testando o envio das informações de cotação, e verificando o status de
        retorno
        """
        self._login()

        values = [
            # Cidade | Indicador | Fonte | Valor | Status da resposta
            [self.jatai.pk, self.soja_balcao.pk, None, 61, 'ERROR'],
            [self.jatai.pk, self.soja_balcao.pk, 999, 62, 'ERROR'],
            [self.jatai.pk, None, self.joao.pk, 63, 'ERROR'],
            [self.jatai.pk, 999, self.joao.pk, 64, 'ERROR'],
            [None, self.soja_balcao.pk, self.joao.pk, 65, 'ERROR'],
            [999, self.soja_balcao.pk, self.joao.pk, 66, 'ERROR'],
            [self.jatai.pk, self.soja_balcao.pk, self.joao.pk, 67, 'ERROR'],
            [self.jatai.pk, self.soja_disponivel.pk, self.joao.pk, 68, 'OK']
        ]

        for line in values:
            data = {
                'date': date.today(),
                'city': line[0],
                'indicator': line[1],
                'source': line[2],
                'value': line[3],
            }

            response = self.client.post(self._get_url(), data)
            msg = response.request['PATH_INFO'] + '?' + \
                  response.request['QUERY_STRING']
            response_json = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_json['status'], line[4], msg)

    def test_post_save_update_delete(self):
        """
        Testando o envio das informações de cotação, e verificando a
        gravação e exclusão de informações
        """
        self._login()

        # Gravando o item a primeira vez(insert)
        data = {
            'date': date.today(),
            'city': self.jatai.pk,
            'indicator': self.soja_disponivel.pk,
            'source': self.joao.pk,
            'value': 68,
        }
        response = self.client.post(self._get_url(), data)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'OK', data)
        quotations = Quotation.objects.filter(date=date.today())
        self.assertEqual(quotations.count(), 1)

        # Gravando o item a segunta vez (update)
        " Marcando a cotação como aprovada para reenviar "
        quotation = Quotation.objects.filter(date=date.today())[0]
        quotation.status = Quotation.STATUS_APPROVED
        quotation.save()

        new_value = 69
        data.update({'value': new_value})
        response = self.client.post(self._get_url(), data)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'OK', data)
        quotations = Quotation.objects.filter(date=date.today())
        self.assertEqual(quotations.count(), 1)
        self.assertEqual(quotations[0].value, new_value)

        " Status deve estar aguardando novamente"
        self.assertEqual(quotations[0].status, Quotation.STATUS_WAITING)

        # Gravando o item com valor zerado (delete)
        data.update({'value': 0})
        response = self.client.post(self._get_url(), data)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['status'], 'OK', data)
        quotations = Quotation.objects.filter(date=date.today())
        self.assertEqual(quotations.count(), 0)

        # @TODO: Fazer validação de valores de máximo e mínimo, com campo force

    def test_only_show_source_with_indicator(self):
        """
        Só mostra fontes que tenham pelo menos um indicador para os
        parametros selecionados
        """
        self._login()

        data = {
            'date': date.today(),
            'category': 2,
            'city': self.palmeiras.pk,
            'indicators': [self.boi.pk]
        }

        response = self.client.get(self._get_url(), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "N/A")  # não mostra jbs
        self.assertContains(response, '<input type="number"', 1)  # minerva
