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
TWILIO = True
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_FROM = os.environ.get('TWILIO_FROM')
