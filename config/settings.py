from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-t5#l3y29)yus1u$0jmsz5m2kjhlwavos3@)*zma+6=$busf$3j"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authentication.apps.AuthenticationConfig",
    "reviews.apps.ReviewsConfig",
    "reviews.templatetags.reviews_extras",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'authentication.validators.ContainsLetterValidator',
    },
    {
        'NAME': 'authentication.validators.ContainsNumberValidator',
    },
]


# Internationalization

LANGUAGE_CODE = "fr-fr"  # Language code used for translations

TIME_ZONE = "Europe/Paris"  # Time zone used by the application

USE_I18N = True  # Activation support for translations

USE_L10N = True  # Enable support for localized date and time formats

USE_TZ = True  # Enable time zone support

STATIC_URL = "static/"  # Basic URL for static files
STATICFILES_DIRS = [BASE_DIR.joinpath('static')]  # Directory of static files

# Default Primary Key Field Type
# Used for new tables created by Django
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'authentication.User'  # Custom template for users

LOGIN_URL = 'login'  # Login Page URL
LOGIN_REDIRECT_URL = 'home'  # Redirect URL after successful login
LOGOUT_REDIRECT_URL = LOGIN_URL  # Redirect URL after successful logout

MEDIA_URL = '/media/'  # Basic URL for media files
MEDIA_ROOT = BASE_DIR / 'media/'  # Répertoire des fichiers média
