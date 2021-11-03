from django import forms
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def ifag_quotation_field(context, source, indicator, city, source_indicator_city,
                         quotations):
    """
    Cria o campo de cotação para o conjunto fonte/indicador/cidade

    :param source:
    :param indicator:
    :param city:
    :param source_indicator_city:
    :param quotations:
    :return: html
    """

    " Definindo o valor inicial, se já ouver um valor de cotação "
    value = None
    rejected = False
    readonly = False
    user = context['user']
    for entity in quotations:
        if entity.source.pk == source.pk and \
                        entity.indicator.pk == indicator.pk and \
                        entity.city.pk == city.pk:
            value = entity.value
            rejected = entity.status == entity.STATUS_REJECTED
            if entity.status == entity.STATUS_APPROVED:
                readonly = not user.has_perm('ifag.can_change_approved_quotation')

    " Definição do campo"
    for entity in source_indicator_city:
        if entity.source.pk == source.pk and \
                        entity.indicator.pk == indicator.pk and \
                        entity.city.pk == city.pk:

            attrs = {
                'data-source': source.pk,
                'data-indicator': indicator.pk,
                'data-city': city.pk,
                'data-decimal_places': 3,
                'class': 'quotationField',

            }
            if readonly:
                attrs.update({
                    'readonly': 'readonly',
                    'style': 'background-color: #eeeeee',
                })

            html_result = forms.NumberInput().render(
                name="quotation-%s-%s-%s" % (source.pk, indicator.pk, city.pk),
                value=value,
                attrs=attrs
            )

            if rejected:
                html_result += '<div style="color:red">Rejeitada</div>'

            return mark_safe(html_result)

    return 'N/A'
