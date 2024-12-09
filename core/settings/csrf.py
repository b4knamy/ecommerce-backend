CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',  'http://localhost:8000', "http://localhost:5173",
]


CSRF_COOKIE_AGE = 604800  # a week
# CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_NAME = "csrf_token"
CSRF_COOKIE_PATH = "/"
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False  # change it to True in production
# CSRF_FAILURE_VIEW
# CSRF_HEADER_NAME
# CSRF_TRUSTED_ORIGINS
# CSRF_USE_SESSIONS
