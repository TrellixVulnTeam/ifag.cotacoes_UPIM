# pylint: skip-file

from .settings import *

SECRET_KEY = '#^dur7@g_m%31vi5&wq)(r1)#e$thqacfm(7jk^p6^lit^p$6@'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ifag_dados_dev',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_dev')

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),
    os.path.join(BASE_DIR, 'ifag/tests/fixtures'),
]
