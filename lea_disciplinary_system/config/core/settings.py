from pathlib import Path
import os
# 📁 Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# 🔐 SECURITY
SECRET_KEY = 'django-insecure-change-me-in-prod'  # Replace this in production!
DEBUG = True # ❌ Turn off in production
ALLOWED_HOSTS = []
  # Add domains/IPs when deploying

# ✅ Installed Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'lea_app',
]

# ✅ Middleware stack
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ URL Configuration
ROOT_URLCONF = 'config.core.urls'

# ✅ Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Place your HTML templates here
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

# ✅ WSGI Application
WSGI_APPLICATION = 'config.core.wsgi.application'

# ✅ Database (SQLite for dev; use PostgreSQL for prod)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ Custom User Model
AUTH_USER_MODEL = 'lea_app.User'

# ✅ Password Validators (disabled in dev for ease)
AUTH_PASSWORD_VALIDATORS = []

# 🌍 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# 🗂️ Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Optional: for custom static dir
STATIC_ROOT = BASE_DIR / 'staticfiles'   # Collect static here for production

# ✅ Default primary key type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# config/core/settings.py

# ... other settings ...

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PHYSICAL_SESSIONS_REQUIRED = 2
ONLINE_SESSIONS_REQUIRED = 3
MEETUP_SESSIONS_REQUIRED = 2
