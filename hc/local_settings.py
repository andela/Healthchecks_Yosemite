import os

DATABASES = {
    'default': {
        'ENGINE':   os.env['DB_ENGINE'],
        'NAME':     os.env['DB_NAME'],
        'USER':     os.env['DB_USER'],
        'PASSWORD': os.env['DB_PASSWORD'],
        'TEST': {'CHARSET': 'UTF8'}
    }
}