
"""
------------------------------------------------------------------------------
 !!CUIDADO!!
 Este arquivo é criado por um template, alterações feitas diretamente, podem
 ser perdidas na configuração de uma nova versão do script
------------------------------------------------------------------------------
"""
from .settings import *

ALLOWED_HOSTS = ['inaes.ifag.org.br', '127.0.0.1', 'localhost', ]
SECRET_KEY = '4@onb391g_%v#9^pjyp@g=*hm+vur@n^d&vfwfx8x(aembn%_l'
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'inaes_ifag_org_br',
        'USER': 'dados_ifag_org_br',
        'PASSWORD': '(h29n3=d9sr-t_43=0lvq+&f2+gq!s37xmbu45+6_eie3)8rwi',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
