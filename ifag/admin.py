from django.conf import settings
from django.contrib import admin
from django.db.models import Max

from .models import *


class IndicatorCityInline(admin.TabularInline):
    model = SourceIndicatorCity
    verbose_name = 'Indicador/Cidade'
    verbose_name_plural = 'Indicadores/Cidades'

    def has_add_permission(self, request):
        return True


class SourceCityInline(admin.TabularInline):
    model = SourceIndicatorCity
    verbose_name = 'Fonte/Cidade'
    verbose_name_plural = 'Fonte/Cidades'

    def has_add_permission(self, request):
        return True


class SourceAdmin(admin.ModelAdmin):
    inlines = [
        IndicatorCityInline,
    ]
    list_filter = [
        'source_indicator__city',
        'source_indicator__indicator',
    ]
    search_fields = [
        'name',
    ]
    fieldsets = (
        ('Principal', {
            'fields': (
                'name',
                'obs',
            ),
        }),
    )


class IndicatorAdmin(admin.ModelAdmin):
    inlines = [
        SourceCityInline,
    ]
    list_filter = [
        'source_indicator__city',
        'source_indicator__source',
    ]
    list_display = ['name', 'unit', 'slug', ]
    search_fields = [
        'name',
    ]

    fieldsets = (
        ('Principal', {
            'fields': (
                'category',
                'name',
                'unit',
                'slug',
            )
        }),
    )


class WithQuotationListFilter(admin.RelatedFieldListFilter):
    """
    Filtro de lista para ser usado nas propriedades de Cotação
    """

    def field_choices(self, field, request, model_admin):
        queryset = QuotationApprove.objects \
            .values_list(field.name, flat=True) \
            .distinct(field.name)

        target_model = field.target_field.model

        queryset = target_model.objects \
            .filter(pk__in=[i for i in queryset]) \
            .order_by('name')

        result = []
        for obj in queryset:
            result.append((obj.pk, obj.name))
        return result


class QuotationApproveAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_filter = [
        ('city', WithQuotationListFilter),
        ('indicator', WithQuotationListFilter),
    ]
    change_list_template = 'ifag/quotation_approve.html'
    list_display = ['city', 'source', 'indicator', 'date', 'value']
    list_display_links = None
    actions = ['approve_selected', 'reject_selected']

    def get_queryset(self, request):
        queryset = super(QuotationApproveAdmin, self).get_queryset(request)
        return queryset.filter(status=Quotation.STATUS_WAITING)

    def approve_selected(self, request, queryset):
        queryset.update(status=Quotation.STATUS_APPROVED)

    def reject_selected(self, request, queryset):
        queryset.update(status=Quotation.STATUS_REJECTED)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class HistoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_filter = [
        ('city', WithQuotationListFilter),
        ('indicator', WithQuotationListFilter),
        'indicator__category'
    ]
    change_list_template = 'ifag/history_list.html'
    show_admin_actions = False
    list_display = ['city', 'indicator', 'date', 'value', 'variation']
    list_display_links = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PublicationAdmin(admin.ModelAdmin):
    change_list_template = 'ifag/publication_list.html'
    show_admin_actions = False
    list_display = ['date', 'create_on', 'create_by']
    list_display_links = None
    actions = ['release']

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] == 'release':
            self.release(request, None)

        if not extra_context:
            extra_context = {}

        extra_context.update({
            'history_count': self.get_num_not_published()
        })

        return super(PublicationAdmin, self) \
            .changelist_view(request, extra_context)

    def get_num_not_published(self):
        """
        Retorna o número de históricos não posteriores a data de
        última publicação
        :return:
        """
        history_qs = History.objects.all()
        max_date = Publication.objects \
            .aggregate(max_date=Max('date'))['max_date']

        if max_date:
            history_qs = history_qs.filter(date__gt=max_date)

        return history_qs.count()

    def release(self, request, queryset):
        """
        Ação que cria o novo release
        """
        try:
            Publication.objects.get(date=date.today())
        except Publication.DoesNotExist:
            entity = Publication()
            entity.create_by = request.user
            entity.date = date.today()
            entity.save()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(City)
admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Unit)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(QuotationApprove, QuotationApproveAdmin)
admin.site.register(Publication, PublicationAdmin)

if settings.DEBUG:
    admin.site.register(SourceIndicatorCity)
