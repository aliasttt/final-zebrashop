from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from decouple import config
import django_heroku
import os

# بارگذاری متغیرهای محیطی
load_dotenv()

# مسیر اصلی پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# امنیت
SECRET_KEY = config('SECRET_KEY', default='&z8!d9b1$u7t^k3@p5g#l1x2q4%f6*r9w+y7z0m!a8p3h2l!q6')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# اپلیکیشن‌ها
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

# میان‌افزارها
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



DATABASES = {  
                           'default': {
                               'ENGINE': 'django.db.backends.sqlite3',
                             'NAME': BASE_DIR / 'db.sqlite3',                 }
                       }


# DATABASES = {
#                            'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}


# پیکربندی استاتیک
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# تنظیمات قالب‌ها
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
            ],
        },
    },
]

# تنظیمات واریز
WSGI_APPLICATION = 'zebrashop.wsgi.application'

# اعتبارسنجی رمز عبور
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

# تنظیمات زبان و منطقه زمانی
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# تنظیمات رسانه‌ها
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# پیکربندی ایمیل
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'aliasadi3853@gmail.com'
EMAIL_HOST_PASSWORD = config("MAIL_HOST_PASSWORD")  # رمز عبور از فایل .env
EMAIL_USE_TLS = True

# تنظیمات احراز هویت
AUTHENTICATION_BACKENDS = [
    'zebrashopapp.backends.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesStandaloneBackend',
]

# مدل کاربری سفارشی
AUTH_USER_MODEL = 'zebrashopapp.RegisterModel'

# تنظیمات خروج
LOGOUT_REDIRECT_URL = 'zebrashopapp:home'

# تنظیمات سشن
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# تنظیمات امنیتی (فقط در حالت تولید)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# محدودیت‌های آدرس‌های ناموفق ورود
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 24

# پیکربندی لاگینگ
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

# فعال‌سازی تنظیمات Heroku
django_heroku.settings(locals())


