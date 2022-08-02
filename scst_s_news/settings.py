import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = '!k%4p0k%2iogplitxwqym@p8o+@j3-tha%e#c)&#+g6kp#i+u9'

DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'account',
    'news',
    'logger',
]

MIDDLEWARE = []

ROOT_URLCONF = 'scst_s_news.urls'
WSGI_APPLICATION = 'scst_s_news.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scst_s_news',
        'USER': os.getenv("MYSQL_USER"),
        'PASSWORD': os.getenv("MYSQL_PASSWORD"),
        'HOST': os.getenv("MYSQL_HOST"),
        'PORT': os.getenv("MYSQL_PORT"),
        'CONN_MAX_AGE': 300,
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_general_ci',
        }
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
STATIC_URL = '/static/'
logging.basicConfig(format='%(levelname)s:%(asctime)s %(pathname)s--%(funcName)s--line %(lineno)d-----%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)