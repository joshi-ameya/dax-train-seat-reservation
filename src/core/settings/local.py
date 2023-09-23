"""
local env settings template.
"""
SECRET_KEY = 'django-insecure-$u-ni+n^=-pz2b)yq5ldd@d60vbh4x2glco%em9$4*n2_ax_f4'
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dax_train_seat_reservation',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True
    }
}
