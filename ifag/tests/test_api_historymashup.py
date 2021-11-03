import json

from django.test import TestCase
from django.urls import reverse

from ifag.models import City, Indicator, History


class ApiHistoryMashupTest(TestCase):
    """ Teste de HistoryMashup """
    fixtures = [
        'city',
        'category',
        'unit',
        'group',
        'indicator',
        'history',
    ]

    def setUp(self):
        """
        Configuração do teste
        """
        " Produtos "
        self.soja_balcao = Indicator.objects.get(slug='soja-balcao')
        self.soja_disponivel = Indicator.objects.get(slug='soja-disponivel')
        self.boi = Indicator.objects.get(slug='boi-gordo')

        " Cidades "
        self.jatai = City.objects.get(name_ascii="JATAI")
        self.palmeiras = City.objects.get(name_ascii="PALMEIRAS DE GOIAS")
        self.goiania = City.objects.get(name_ascii="GOIANIA")
        self.rio_verde = City.objects.get(name_ascii="RIO VERDE")

        self.url = reverse('ifag-api:historymashup-list')

    def _test_format(self, response_json):
        """
        Testa se o formato da resposta está no padrão

        response_json = [{
            'indicator': {
                'slug': 'boi-gordo',
                'name': 'Boi Gordo'
            },
            'lower_avg': 80,
            'lower_avg_city': {
                'pk': 1,
                'uf': 'GO',
                'name': 'Rio Verde'
            },
            'higher_avg': 150,
            'higher_avg_city': {
                'pk': 2,
                'uf': 'GO',
                'name': 'Acreúna'
            },
            'avg': 100,
            'variation': 2.1,
        }]
        """

        for linha in response_json:
            " Testando conteúdo da raiz "
            root_keys = [
                'indicator', 'lower_avg', 'lower_avg_city', 'higher_avg',
                'higher_avg_city', 'avg', 'date', 'variation'
            ]
            self.assertListEqual(
                sorted(list(linha.keys())),
                sorted(root_keys)
            )

            " Testando conteúdo do indicador "
            indicator_keys = ['name', 'pk', 'slug', 'unit']
            self.assertListEqual(
                sorted(list(linha.get('indicator').keys())),
                sorted(indicator_keys)
            )

            " Testando conteúdo das cidades "
            city_keys = ['pk', 'name', 'uf']
            self.assertListEqual(
                sorted(list(linha.get('lower_avg_city').keys())),
                sorted(city_keys)
            )
            self.assertListEqual(
                sorted(list(linha.get('higher_avg_city').keys())),
                sorted(city_keys)
            )

    def test_get_sem_parametro(self):
        """ Sem parametro deve devolver uma lista vazia e status 200 """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_get_com_data(self):
        """ Com data e sem indicador deve devolver todos """
        response = self.client.get(self.url, {'date': '2017-09-04'})
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 2)
        self._test_format(response_json)

    def test_get_com_data_indicador(self):
        """
        Com data e com indicador deve devolver somente informações daquele
        indicador
        """
        data = {
            'date': '2017-09-04',
            'indicator': ','.join([
                self.soja_disponivel.slug,
            ])
        }
        response = self.client.get(self.url, data)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 1)
        self._test_format(response_json)

    def test_get_com_data_indicadores(self):
        """
        Com data e com mais de um indicador deve devolver informações de todos
        os indicadores informados
        """
        data = {
            'date': '2017-09-04',
            'indicator': ','.join([
                self.soja_disponivel.slug,
                self.soja_balcao.slug
            ])
        }

        response = self.client.get(self.url, data)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 2)
        self._test_format(response_json)

        # Cidade Maior e menor devem ser diferentes
        self.assertNotEqual(
            response_json[0]['lower_avg_city']['pk'],
            response_json[0]['higher_avg_city']['pk'],
            'Pelo conjunto de dados, a cidade com média maior e menor '
            'não podem ser a mesma'
        )

    def test_get_com_data_indicadores_cidade(self):
        """
        Com data e com mais de um indicador deve devolver informações de todos
        os indicadores informados
        """
        data = {
            'date': '2017-09-04',
            'city': self.jatai.pk,
            'indicator': ','.join([
                self.soja_disponivel.slug,
                self.soja_balcao.slug
            ])
        }
        response = self.client.get(self.url, data)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), 2)
        self._test_format(response_json)

        # Cidade Maior e menor devem ser Jataí
        self.assertEqual(
            response_json[0]['lower_avg_city']['pk'],
            self.jatai.pk
        )
        self.assertEqual(
            response_json[0]['higher_avg_city']['pk'],
            self.jatai.pk
        )

        # Valores de media, minimo e máximo devem ser iguais
        self.assertEqual(
            response_json[0]['lower_avg'],
            response_json[0]['avg']
        )
        self.assertEqual(
            response_json[0]['higher_avg'],
            response_json[0]['avg']
        )

        # Se informar cidade, nunca devolve outra, mesmo com o valor igual
        cities = [
            self.jatai.pk,
            self.goiania.pk,
            self.palmeiras.pk,
            self.rio_verde.pk
        ]
        for city in cities:
            data = {
                'date': '2017-09-04',
                'city': city,
                'indicator': self.soja_disponivel.slug
            }
            entity = History.objects.get(
                date='2017-09-04',
                city__pk=city,
                indicator__slug=self.soja_disponivel.slug
            )
            response = self.client.get(self.url, data)
            response_json = json.loads(response.content)
            self.assertEqual(
                response_json[0]['higher_avg_city']['pk'],
                response_json[0]['lower_avg_city']['pk'],
            )
            self.assertEqual(
                response_json[0]['higher_avg_city']['pk'],
                city
            )
            self.assertEqual(
                float(response_json[0]['higher_avg']),
                float(entity.value)
            )
            self.assertEqual(
                float(response_json[0]['lower_avg']),
                float(entity.value)
            )
            self.assertEqual(
                float(response_json[0]['avg']),
                float(entity.value)
            )
            self.assertEqual(
                float(response_json[0]['variation']),
                float(entity.variation)
            )

