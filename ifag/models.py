from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import formats
from django.utils.encoding import force_text
from unidecode import unidecode


class CityManager(models.Manager):
    def get_has_indicator(self):
        return self.filter(source_indicator__isnull=False).distinct()


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    name_ascii = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    objects = CityManager()

    def __str__(self):
        return '{}-{}'.format(self.name, self.uf)

    def save(self, *args, **kwargs):
        self.name_ascii = unidecode(self.name)
        return super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['name_ascii']


class Category(models.Model):
    """Categoria de indicador econômico"""
    name = models.CharField(max_length=100, verbose_name='nome')
    default = models.BooleanField(
        verbose_name='padrão',
        help_text='Categoria principal nos formulários do sistema'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Group(models.Model):
    """Grupo de indicador econômico"""
    name = models.CharField(max_length=100, verbose_name='nome')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Grupo de Indicador'
        verbose_name_plural = 'Grupos de Indicadores'


class Unit(models.Model):
    """Unidade de medida"""
    name = models.CharField(max_length=100, verbose_name='nome')
    symbol = models.CharField(max_length=9, verbose_name='símbolo')

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.symbol)

    class Meta:
        verbose_name = 'Unidade de Medida'
        verbose_name_plural = 'Unidades de Medida'


class Indicator(models.Model):
    """Indicador econômico"""
    name = models.CharField(verbose_name='nome', max_length=100, unique=True)
    category = models.ForeignKey(Category, verbose_name='Categoria')
    unit = models.ForeignKey(Unit, verbose_name='Unidade de Medida')
    slug = models.SlugField(
        max_length=128,
        blank=True,
        unique=True,
        editable=True,
        verbose_name='permalink',
        help_text='Identificação única do indicador para as APIS'
    )

    # Agrupamento
    group = models.ForeignKey(
        Group,
        verbose_name='Grupo',
        null=True,
        blank=True,
    )
    group_short_name = models.CharField(
        verbose_name='abreviação',
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text='Nome curto dentro do grupo. Ex: "0-12 Meses"'
    )
    group_order = models.SmallIntegerField(
        verbose_name='ordem de apresentação',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Indicador Econômico'
        verbose_name_plural = 'Indicadores Econômicos'
        unique_together = (('group', 'group_order',),)
        ordering = ['name', ]

    def _create_slug(self):
        """ Lógica para criação do slug """
        slug = slugify(self.name)
        while True:
            try:
                article = Indicator.objects.get(slug=slug)
                if article == self:
                    break
                else:
                    slug = slug + '-'
            except:
                break
        return slug

    def save(self, *args, **kwargs):
        """ Sobrescreve o save padrão para chamar a criação do slug """
        if not self.slug:
            self.slug = self._create_slug()

        return super(Indicator, self).save(*args, **kwargs)


class Source(models.Model):
    """Fonte de informação"""
    name = models.CharField(verbose_name='nome', max_length=100, unique=True)
    obs = models.TextField(verbose_name='observações', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fonte de Informação'
        verbose_name_plural = 'Fontes de Informação'
        ordering = ['name', ]


class SourceIndicatorCity(models.Model):
    """ Fonte/Indicador/Cidade """
    source = models.ForeignKey(
        Source,
        verbose_name='fonte',
        related_name='source_indicator',
    )
    indicator = models.ForeignKey(
        Indicator,
        verbose_name='indicador',
        related_name='source_indicator',
    )
    city = models.ForeignKey(
        City,
        verbose_name='cidade',
        related_name='source_indicator',
    )

    def __str__(self):
        return '{}/{}/{}'.format(self.source, self.indicator, self.city)

    class Meta:
        unique_together = (
            ('source', 'indicator', 'city'),
        )
        verbose_name = 'Fonte/Indicador/Cidade'
        verbose_name_plural = 'Fontes/Indicadores/Cidades'


class Quotation(models.Model):
    """ Cotação """
    source = models.ForeignKey(Source, verbose_name='fonte')
    indicator = models.ForeignKey(Indicator,
                                  verbose_name='indicador econômico')
    city = models.ForeignKey(City, related_name='quotation',
                             verbose_name='cidade')
    date = models.DateField(verbose_name='data', blank=True)
    value = models.DecimalField(
        verbose_name='valor',
        max_digits=7,
        decimal_places=3
    )
    create_on = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True,
    )

    STATUS_WAITING = 'waiting'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUSES = (
        (STATUS_WAITING, 'aguardando'),
        (STATUS_APPROVED, 'aprovado'),
        (STATUS_REJECTED, 'rejeitado'),
    )

    status = models.CharField('Status', max_length=8, default=STATUS_WAITING)

    def get_status_display(self):
        """ Recupera o status de acordo com a propriedade 'status'"""
        return force_text(
            dict(Quotation.STATUSES).get(self.status, None),
            strings_only=True
        )

    calculated = models.BooleanField(
        verbose_name='Calculado?',
        default=False,
        help_text='Se já gerou a média desta cotação',
    )

    def __str__(self):
        return '{}/{}/{}/{}'.format(
            self.source,
            self.indicator,
            self.city,
            self.date,
        )

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()

        return super(Quotation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cotação'
        verbose_name_plural = 'Cotações'
        permissions = (
            ('can_add_quotation', 'Add Quotation'),
            ('can_change_approved_quotation', 'Change Approved Quotation'),
        )


class QuotationApprove(Quotation):
    class Meta:
        verbose_name = 'cotação'
        verbose_name_plural = 'aprovar cotações'
        permissions = (
            ('can_approve_quotation', 'Approve Quotation'),
        )
        proxy = True


class History(models.Model):
    """Histórico do indicador"""
    indicator = models.ForeignKey(Indicator,
                                  verbose_name='indicador econômico')
    city = models.ForeignKey(City, verbose_name='cidade',
                             related_name='history')
    date = models.DateField(verbose_name='data', blank=True)
    value = models.DecimalField(
        verbose_name='valor',
        max_digits=7,
        decimal_places=3
    )
    variation = models.DecimalField(
        verbose_name='variação',
        max_digits=7,
        decimal_places=2,
        default=0
    )
    create_on = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True,
    )

    def __str__(self):
        return '{}/{}/{}'.format(
            self.indicator,
            self.city,
            self.date,
        )

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()

        return super(History, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Histórico de Indicador'
        verbose_name_plural = 'Históricos de Indicadores'


class Publication(models.Model):
    """Publicação dos históricos"""
    date = models.DateField(verbose_name='data', blank=True)
    create_on = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True,
    )
    create_by = models.ForeignKey(User, verbose_name='Criado por')

    def __str__(self):
        return formats.date_format(self.date, "SHORT_DATE_FORMAT")

    class Meta:
        verbose_name = 'Publicação de Histórico'
        verbose_name_plural = 'Publicações de Históricos'
