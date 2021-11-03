# pylint: skip-file
from django.conf import settings
from django.conf.urls import include, static, url
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

# Text to put at the end of each page's <title>.
admin.site.site_title = 'IFAG Econômico'

# Text to put in each page's <h1>.
admin.site.site_header = 'IFAG Econômico'

# Text to put at the top of the admin index page.
admin.site.index_title = 'Administração'

urlpatterns = [
    # Django JET
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS

    # Django JET dashboard URLS
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    # Urls do IFAG
    url(r'^ifag/', include('ifag.urls', namespace='ifag')),

    # Urls das apis do IFAG
    url(r'^ifag/api/', include('ifag.api.urls', namespace='ifag-api')),

    # Urls do admin
    url(r'^', admin.site.urls),

    # Redefinição do password
    url(
        r'^recuperar-senha/$',
        password_reset,
        name='admin_password_reset'
    ),
    url(
        r'^recuperar-senha/feito/$',
        password_reset_done,
        name='password_reset_done'
    ),
    url(
        r'^redefinir/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(
        r'^redefinir/feito/$',
        password_reset_complete,
        name='password_reset_complete'
    ),

    # # Qualquer url nao listada, redireciona para admin
    # url(
    #     r'^.*$',
    #     RedirectView.as_view(
    #         url=reverse_lazy('admin:index'),
    #         permanent=True
    #     ),
    #     name='index404'
    # ),
]

urlpatterns += static.static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

urlpatterns += static.static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
