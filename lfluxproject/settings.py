# Django settings for lfluxproject project.
gettext = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

# you want to change this in localsettings
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# you want to change this in localsettinsg
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
# you want to change this in localsettings.
SECRET_KEY = None


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('de', gettext('German')),
    ('en', gettext('English')),
)


# from
# http://morethanseven.net/2009/02/11/
# django-settings-tip-setting-relative-paths.html

import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'localstatic')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'static'),
)

LOCALE_PATHS = (os.path.join(SITE_ROOT,'conf/locale'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'lfluxproject.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'django.contrib.markup',

    'debug_toolbar',

    'ltools', # overrides some imported templates

    'pagedown',
    'south',
    'taggit',
    'reversion',

    'crispy_forms',     # for tumblelog
    'tumblelog',


    'userena',
    'guardian',         # for userena
    'easy_thumbnails',  # for userena

    'django_nose',
    'django_extensions',

    'lstory',
    'limage',
    'lprofile',
    'ladmin',           # admin overrides & extensions.

    'django.contrib.comments',
    'voting',
    'threadedcomments',

    'lqa',

    'django.contrib.flatpages',
    'google_analytics',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',  # required by django-admin-tools

    'lfluxproject.context_processors.settings_processor',
    'lfluxproject.context_processors.tracking_processor',
    'lfluxproject.context_processors.site_processor',
    'lfluxproject.context_processors.flatcontent',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


ADMIN_TOOLS_INDEX_DASHBOARD = {
    'ladmin.admin.admin': 'lfluxproject.dashboard.CustomIndexDashboard',
    'django.contrib.admin.site': 'admin_tools.dashboard.DefaultIndexDashboard'
}

CRISPY_TEMPLATE_PACK = 'uni_form'
COMMENTS_APP = 'threadedcomments'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# you should change this in your local settings.

TUMBLELOG_TYPEIMAGES = True
TUMBLELOG_PARENT_MODEL = 'lstory.Story'


ANONYMOUS_USER_ID = -1  # required by guardian?

AUTH_PROFILE_MODULE = 'lprofile.Profile'
LOGIN_URL = '/user/signin/'
LOGOUT_URL = '/user/signout/'
USERENA_REDIRECT_ON_SIGNOUT = '/'
USERENA_SIGNIN_REDIRECT_URL = '/user/%(username)s/'

DEMO_MODE = False  # make all users admin per default

EMBEDLY_KEY = None # OVERRIDE THIS
EMBEDLY_MAXWIDTH = 300

SOUTH_TESTS_MIGRATE = False

GOOGLE_ANALYTICS_ACCOUNT_CODE = False
