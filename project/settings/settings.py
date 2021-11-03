# pylint: skip-file

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['dados.ifag.org.br', '127.0.0.1', 'localhost', ]

# Application definition

INSTALLED_APPS = [
    # Django Jet
    # 'jet.dashboard',
    'jet',

    # Apps padrões
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_propeller',
    'rest_framework',
    'corsheaders',

    # App do ifag
    'ifag',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

# class InvalidTemplateVariable(str):
#     def __mod__(self, other):
#         from django.template.base import TemplateSyntaxError
#         raise TemplateSyntaxError("Invalid variable : '%s'" % other)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            # 'string_if_invalid': InvalidTemplateVariable("%s"),
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        # Não deve existir banco válido no arquivo principal
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# noinspection PyUnresolvedReferences
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'dados.ifag.org.br',
    'ifag.org.br',
    'localhost:63342',
    '127.0.0.1:8000',
    '127.0.0.1:5000',
)

JET_SIDE_MENU_COMPACT = True  # Sem submenus
# JET_DEFAULT_THEME = 'light-gray'
# JET_DEFAULT_THEME = 'light-green'
# JET_DEFAULT_THEME = 'light-violet'
# JET_DEFAULT_THEME = 'light-blue'
JET_DEFAULT_THEME = 'green'

JET_SIDE_MENU_ITEMS = [
    {
        'label': '',
        'items': [
            {
                'label': 'Registrar cotações',
                'url': '/ifag/quotationinsert/',
                'permissions': {'ifag.can_add_quotation'}
            },
            {
                'name': 'ifag.quotationapprove',
                'permissions': {'ifag.can_approve_quotation'}
            },
            {
                'name': 'ifag.history',
                'permissions': {'ifag.change_history'}
            },
            {
                'name': 'ifag.publication',
                'permissions': {'ifag.change_publication'}
            },
        ]
    },
    {
        'label': 'Cadastros',
        'items': [
            {
                'name': 'ifag.indicator',
                'permissions': {'ifag.change_indicator'}
            },
            {
                'name': 'ifag.source',
                'permissions': {'ifag.change_source'}
            },
            {
                'name': 'ifag.category',
                'permissions': {'ifag.change_category'}
            },
            {
                'name': 'ifag.unit',
                'permissions': {'ifag.change_unit'}
            },
            {
                'name': 'auth.user',
                'label': 'Usuários do Sistema',
                'permissions': {'auth.change_user'}
            },
            {
                'name': 'auth.group',
                'label': 'Grupos de Usuários',
                'permissions': {'auth.change_group'}
            },
        ]
    },
]

JQUERY_URL = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
