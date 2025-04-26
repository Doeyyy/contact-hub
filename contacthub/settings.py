from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-%hjisw!0c0)bs&s9m#0e(#(=g54-#f+q2-d3+p%puk)0=5qrp#'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'contacts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'contacthub.urls'

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

WSGI_APPLICATION = 'contacthub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        # default='postgresql://postgres:postgres@localhost:5432/mysite', WE USE THIS PRODUCTION
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/ 'staticfiles'#we need this for render

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'contacts.User'
LOGIN_URL = '/admin/'

INSTALLED_APPS += ["storages"]
STORAGES = {
    "default":{
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles":{
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
    # "staticfiles": { "django.contrib.staticfiles.storage.StaticFilesStorage" ,} ORIGO, MOD FOR WHITENOISE RENDER
}

# Backblaze B2 configuration
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Use your actual credentials
AWS_ACCESS_KEY_ID = "0051c57ead2f6ee0000000001"
AWS_SECRET_ACCESS_KEY = "K005Qu4zTLQB2hbhJmS5wtTlQv+MW+o"
AWS_STORAGE_BUCKET_NAME = "Contacthubx"

# Make sure this is your actual endpoint - get this from your Backblaze B2 bucket details
AWS_S3_ENDPOINT_URL = "https://s3.us-east-005.backblazeb2.com"

# This should match the region in your endpoint URL
AWS_S3_REGION_NAME = "us-east-005"

# Required settings for B2
AWS_S3_ADDRESSING_STYLE = "virtual"

# Use the same region as in your endpoint URL
AWS_S3_CUSTOM_DOMAIN = f"Contacthubx.s3.us-east-005.backblazeb2.com"

# File permissions
AWS_DEFAULT_ACL = "public-read"  # Change to "private" if files should be private
AWS_S3_FILE_OVERWRITE = False



AWS_QUERYSTRING_AUTH = False  # False = public files, True = signed URLs
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
