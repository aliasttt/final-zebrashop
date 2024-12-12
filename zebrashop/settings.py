from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
from decouple import config
import django_heroku
django_heroku.settings(locals())



load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-$qkj2*yk9c)*f3z#yo1%b=5s%0p1sxt8qlsn-lhto9wmy)h(_)'
SECRET_KEY = config('SECRET_KEY',default = '&z8!d9b1$u7t^k3@p5g#l1x2q4%f6*r9w+y7z0m!a8p3h2l!q6')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'zebrashop.com.tr',
    '185.208.181.154',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'zebrashopapp',
    'crispy_forms',
    'crispy_bootstrap5',
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'zebrashop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 #'zebrashopapp.context_processors.user_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'zebrashop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {  
#                           'default': {
#                               'ENGINE': 'django.db.backends.sqlite3',
#                             'NAME': BASE_DIR / 'db.sqlite3',                 }
#                       }


DATABASES = {
                           'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
                       }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'  # باید با اسلش شروع شود

STATICFILES_DIRS = [
    BASE_DIR / "static",  # مسیر دایرکتوری استاتیک شما
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aliasadi3853@gmail.com'
EMAIL_HOST_PASSWORD = 'spplwkgtxdfrurpe'
EMAIL_USE_TLS = True



import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



AUTHENTICATION_BACKENDS = [
    'zebrashopapp.backends.PhoneBackend',  # مسیر درست به Backend خود را وارد کنید
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesStandaloneBackend',
]

AUTH_USER_MODEL = 'zebrashopapp.RegisterModel'

LOGOUT_REDIRECT_URL = 'zebrashopapp:home'


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # ذخیره session در دیتابیس
SESSION_COOKIE_AGE = 1209600  # طول عمر session (در ثانیه، اینجا دو هفته)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # پایان session با بسته شدن مرورگر



CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# pip freeze > requirements.txt

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True


SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True


X_FRAME_OPTIONS = 'DENY'



AXES_FAILURE_LIMIT = 5  # تعداد دفعات تلاش ناموفق قبل از مسدودسازی
AXES_COOLOFF_TIME = 24  # زمان مسدودسازی به ساعت






LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}