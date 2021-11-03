from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from .forms import QuotationSearch, QuotationForm
from .models import Quotation, Source, SourceIndicatorCity


@method_decorator(csrf_exempt, name='dispatch')
class QuotationInsert(PermissionRequiredMixin, FormView):
    login_url = reverse_lazy('admin:login')
    model = Quotation
    context_object_name = "result"
    paginate_by = 20
    template_name = 'ifag/quotation_insert.html'
    permission_required = 'ifag.can_add_quotation'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = {}

        search_form = QuotationSearch(
            self.request.GET if len(self.request.GET) else None
        )
        if search_form.is_valid():
            context.update(search_form.cleaned_data)
            qs = SourceIndicatorCity.objects.filter(
                indicator__in=search_form.cleaned_data['indicators'],
            )
            context['source_indicator_city'] = qs

            # Exibe somente as fontes que existem na cidade
            if search_form.cleaned_data.get('city'):
                qs = qs.filter(
                    city=search_form.cleaned_data.get('city')
                )
            context['sources'] = Source.objects.filter(
                pk__in=qs.values('source').distinct()
            )

            context['quotations'] = search_form.get_queryset()

        context['search_form'] = search_form

        return context

    def post(self, request, *args, **kwargs):
        """
        Rotina de salvamento dos inputs de cotação
        """
        result = {
            'status': None,
            'message': None,
        }

        form = QuotationForm(request.POST)
        if form.is_valid():
            form.save()
            result.update({'status': 'OK'})
        else:
            result.update({'status': 'ERROR', 'message': form.errors, })

        return JsonResponse(result)
