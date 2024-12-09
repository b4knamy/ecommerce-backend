
# CLIENT INFORMATIONS
from os import getenv

CLIENT_OWNER_SITE_DOMAIN = "http://localhost:5173"
CLIENT_OWNER_SITE_BACKEND = "http://localhost:8000"
CLIENT_OWNER_SITE_HEADER = "Óculos de Fábrica"
CLIENT_OWNER_SITE_TITLE = "Óculos de Fábrica"

FILE_UPLOAD_MAX_MEMORY_SIZE_MB = 2
FILE_UPLOAD_MAX_MEMORY_SIZE = FILE_UPLOAD_MAX_MEMORY_SIZE_MB * 1024 * 1024
MAX_FILE_PER_COMMENT = 3
MAX_SEARCH_PRODUCT_PER_PAGE = 5
MAX_COMMENT_PER_PAGE = 5
MAX_GLASSES_PER_PAGE = 15

STRIPE_SECRET_KEY_TEST = getenv("STRIPE_SECRET_KEY_TEST", "")

STRIPE_WEBHOOK_SECRET_KEY = getenv("STRIPE_WEBHOOK_SECRET_KEY", "")
