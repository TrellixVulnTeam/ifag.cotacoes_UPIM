# pylint: skip-file
from datetime import date
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget, \
    FilteredSelectMultiple

from .models import Category, City, Indicator, Quotation, SourceIndicatorCity


class QuotationSearch(forms.Form):
    date = forms.DateField(label='Data', widget=AdminDateWidget())

    category = forms.ModelChoiceField(
        Category.objects.all(),
        empty_label=None,
        label='Categoria',
    )
    city = forms.ModelChoiceField(
        City.objects.get_has_indicator(),
        label='Cidades',
    )

    indicators = forms.ModelMultipleChoiceField(
        Indicator.objects.all(),
        widget=FilteredSelectMultiple("indicadores", is_stacked=True),
        label="Indicadores"
    )

    def __init__(self, data=None, initial=None, **kwargs):
        super(QuotationSearch, self).__init__(
            data=data,
            initial=initial,
            **kwargs
        )

        """
        Valores iniciais dos campos
        """
        if not self.initial.get('category'):
            self.initial.update({'category': 1})

        if not self.initial.get('date'):
            self.initial.update({'date': date.today()})

        """
        Dados preenchido nos campos
        """
        if self.data:
            qs = Indicator.objects.all()

            # se tiver categoria
            if self.data.get('category'):
                " Filtrando os indicadores "
                qs = qs.filter(category__pk=self.data.get('category'))

                " Filtrando as cidades "
                filters = {
                    'source_indicator__indicator__category__pk':
                        self.data.get('category')
                }
                self.fields["city"].queryset = City.objects \
                    .filter(**filters) \
                    .distinct()

            # se tiver cidade
            if self.data.get('city'):
                qs = qs.filter(
                    source_indicator__city__pk=self.data.get('city')
                )

            self.fields["indicators"].queryset = qs.distinct()

    def get_queryset(self):
        """
        Filtra o queryset de cotações com os valores preenchidos

        :return: QuotationManager
        """

        if not self.is_valid():
            raise Exception(self.errors)

        qs = Quotation.objects.all()

        if self.cleaned_data.get('date'):
            qs = qs.filter(
                date=self.cleaned_data.get('date')
            )

        if self.cleaned_data.get('indicators'):
            qs = qs.filter(
                indicator__in=self.cleaned_data.get('indicators')
            )

        if self.cleaned_data.get('city'):
            qs = qs.filter(
                city__pk=self.cleaned_data.get('city').pk
            )

        return qs

    @property
    def media(self):
        media = super(QuotationSearch, self).media
        extra = '' if settings.DEBUG else '.min'
        js = [
            'core.js',
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
            'admin/RelatedObjectLookups.js',
            'actions%s.js' % extra,
            'urlify.js',
            'prepopulate%s.js' % extra,
            'vendor/xregexp/xregexp%s.js' % extra,
        ]

        media.add_js(['admin/js/%s' % url for url in js])

        return media


class QuotationForm(forms.ModelForm):
    force = forms.BooleanField(required=False, )

    def __init__(self, *args, **kwargs):
        super(QuotationForm, self).__init__(*args, **kwargs)
        self.fields['value'].required = False

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > date.today():
            raise forms.ValidationError("Não permitido lançar em data futura")
        return date

    def clean(self):
        if 'source' not in self.cleaned_data:
            return None
        if 'indicator' not in self.cleaned_data:
            return None
        if 'city' not in self.cleaned_data:
            return None

        try:
            SourceIndicatorCity.objects.get(
                source=self.cleaned_data['source'],
                indicator=self.cleaned_data['indicator'],
                city=self.cleaned_data['city'],
            )
        except SourceIndicatorCity.DoesNotExist:
            raise forms.ValidationError(
                "Conjundo de Fonte / Indicador / Cidade não encontrado."
            )

    def save(self, commit=True):
        model = self._meta.model

        try:
            instance = model.objects.get(
                date=self.cleaned_data['date'],
                source=self.cleaned_data['source'],
                indicator=self.cleaned_data['indicator'],
                city=self.cleaned_data['city'],
            )
        except model.DoesNotExist:
            instance = model(
                date=self.cleaned_data['date'],
                source=self.cleaned_data['source'],
                indicator=self.cleaned_data['indicator'],
                city=self.cleaned_data['city'],
            )

        # Se o valor for zerado deleta
        if not self.cleaned_data['value']:
            return instance.delete()

        # Atualiza o valor
        instance.value = self.cleaned_data['value']
        instance.status = Quotation.STATUS_WAITING
        instance.calculated = False

        if commit:
            instance.save()
            self._save_m2m()

        return instance

    class Meta:
        model = Quotation
        fields = ['source', 'indicator', 'city', 'date', 'value', 'force', ]
