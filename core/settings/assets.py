from .environment import DATA_DIR

STATIC_URL = '/static/'
STATIC_ROOT = DATA_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'
