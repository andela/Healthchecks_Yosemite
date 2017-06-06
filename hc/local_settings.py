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
DJMAIL_REAL_BACKEND = 'django_ses_backend.SESBackend'
AWS_SES_ACCESS_KEY_ID = 'foo'
AWS_SES_SECRET_ACCESS_KEY = "bar"
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
