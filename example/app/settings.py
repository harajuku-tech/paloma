# Django settings for example project.
import sys,os
#
PROJECT_DIR=os.path.dirname( os.path.abspath(__file__))
#
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'paloma',                      # Or path to database file if using sqlite3.
        'USER': 'paloma',                      # Not used with sqlite3.
        'PASSWORD': 'paloma',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_CHARSET': 'utf8',
        'TEST_DATABASE_COLLATION': 'utf8_general_ci',
    }
#    #:- this secondary database is for postfix-mysql 
#    ,'postfix': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'postfix',                      # Or path to database file if using sqlite3.
#        'USER': 'postfix',                      # Not used with sqlite3.
#        'PASSWORD': 'postfix',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'js-jp'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'static'),

)

# List of finder classes that know how to find static files in

# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%p!7=*6v2ldki!z(wu0@gr--g_f!6*vh)-+imd7cf29o$gt2^h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'app.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'app.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

######## Custom Configuration 

# - south for data migration
if 'test' not in sys.argv:
    #: Use south after celery related tables are created.
    INSTALLED_APPS +=('south',)  #: for Model Migration
    pass

# - django-celery for asynchoronous task queue
#
INSTALLED_APPS += ('djcelery','kombu.transport.django',)
#: Broker
#BROKER_URL="django://"
#BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'amqp://paloma:paloma@localhost:5672/paloma'
#BROKER_URL = 'redis://localhost:6379/0'
#BROKER_URL = 'mongodb://localhost:27017/paloma'
#
#CELERY_ALWAYS_EAGER = True  #:True: synchronous
#: Serializer
#CELERY_TASK_SERIALIZER='json'
CELERY_TASK_SERIALIZER='pickle'
#: Persistent Worker State
CELERYD_STATE_DB=os.path.join(PROJECT_DIR,'celery_state.db')
#
import djcelery
djcelery.setup_loader()

#CELERY_EMAIL_TASK_CONFIG = {
#    'queue' : 'django_email',
#    'delivery_mode' : 1, # non persistent
#    'rate_limit' : '50/m', # 50 emails per minute
#}

# --- Paloma Configuration
#
INSTALLED_APPS +=('paloma',)  #: this project.
#
SMTP_EMAIL_BACKEND='paloma.backends.SmtpEmailBackend'
#
from kombu import Exchange, Queue
CELERY_DEFAULT_QUEUE = 'paloma'
CELERY_QUEUES = ( 
    Queue('paloma', Exchange('paloma'), routing_key='paloma'),
)

# - paloma for mail transfer agents
if 'test' not in sys.argv:
    EMAIL_BACKEND = 'paloma.backends.PalomaEmailBackend'
#    EMAIL_BACKEND = 'paloma.backends.JournalEmailBackend'
else:
    #: in testing. save messages directory to Journal model
    EMAIL_BACKEND = 'paloma.backends.JournalEmailBackend'

 
# -- sample app

INSTALLED_APPS +=(
        'app.accounts', #: Sample Membership Management
        'app.foods',    #:  Sammple application for Paloma
        ) 

# -- django-extensinon

INSTALLED_APPS +=('django_extensions',)  #:  tools for django-extensions

# - logging
import applogs
applogs.config(LOGGING)

# - mandb for MySQL command shortcuts

INSTALLED_APPS +=('mandb',)  #:  tools for MySQL

