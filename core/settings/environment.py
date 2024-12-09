from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(dotenv_path=BASE_DIR / "dotenv_files" / ".env")

DATA_DIR = BASE_DIR.parent / "data" / "web"

SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-e9(a_c2oa!l+66ptbr!8qsuupd_pr(r_xc&g6rk9sx@_zy*8$s")

DEBUG = bool(int(os.getenv("DEBUG", 0)))


ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS", "").split(",") if h.strip()]

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_SETTINGS_MODULE = "core.settings"

AUTH_USER_MODEL = "authentication.User"

APPEND_SLASH = False


# CLIENT INFORMATIONS

CLIENT_OWNER_SITE_DOMAIN = "http://localhost:3000"
CLIENT_OWNER_SITE_HEADER = "Óculos de Fábrica"
CLIENT_OWNER_SITE_TITLE = "Óculos de Fábrica"
