from .environment import BASE_DIR

import os

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        'NAME': os.getenv("POSTGRES_DB", "postgresql_db"),
        'USER': os.getenv("POSTGRES_USER", "postgres"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "heronosso"),
        'HOST': os.getenv("POSTGRES_HOST", "postgresql_db"),
        'PORT': os.getenv("POSTGRES_PORT", "5432"),
    },
    'test_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}