# settings.py
from os import getenv

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP backend
EMAIL_HOST = 'smtp.gmail.com'  # For Gmail
EMAIL_PORT = 587  # For TLS
EMAIL_USE_TLS = True  # Use TLS
EMAIL_HOST_USER = getenv("EMAIL_ADDRESS", "")  # Your email address
# Your email password (consider using an app password for Gmail)
EMAIL_HOST_PASSWORD = getenv("EMAIL_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default sender email
