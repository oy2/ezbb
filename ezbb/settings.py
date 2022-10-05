####################################################################
# ezbb Django Settings -- See Django Docs                          #
# Always change marked settings before deploying, and put behind   #
# a proxy like nginx with tls!                                     #
####################################################################

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


####################################################################
# ALWAYS CHANGE SECRET KEY BEFORE DEPLOYING TO PRODUCTION          #
####################################################################
SECRET_KEY = 'django-insecure-zdk&n40u&ke_23qq954k@-8h_*kx+ea0!7q))w6i^*i@n-&ige'  # CHANGE ME! #
####################################################################
# ALWAYS TURN DEBUG OFF BEFORE DEPLOYING TO PRODUCTION             #
####################################################################
DEBUG = True  # CHANGE ME! #
####################################################################
# ALWAYS DEFINE ALLOWED HOSTS BEFORE DEPLOYING TO PRODUCTION       #
####################################################################
ALLOWED_HOSTS = [  # CHANGE ME! #
]

####################################################################
# Application definition                                           #
####################################################################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    # forum
    'forum.apps.ForumConfig',
    # accounts
    'accounts.apps.AccountsConfig',
]

####################################################################
# Middleware configuration                                         #
####################################################################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

####################################################################
# Root URL Configuration for ezbb                                  #
####################################################################
ROOT_URLCONF = 'ezbb.urls'

####################################################################
# Templates Configuration                                          #
####################################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ezbb.wsgi.application'

####################################################################
# DATABASE -- CONSIDER USING A PROPER DATABASE INSTEAD OF SQLITE3  #
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases    #
####################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

####################################################################
# Password validation                                              #
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
####################################################################
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

####################################################################
# Configuration for Login and Logout views (see accounts/urls.py)  #
####################################################################
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

####################################################################
# Internationalization                                             #
# https://docs.djangoproject.com/en/4.1/topics/i18n/               #
####################################################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

####################################################################
# Static files (CSS, JavaScript, Images)                           #
# https://docs.djangoproject.com/en/4.1/howto/static-files/        #
####################################################################
STATIC_URL = 'static/'

####################################################################
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
####################################################################
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
