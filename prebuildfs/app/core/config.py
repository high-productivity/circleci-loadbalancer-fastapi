import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
from databases import DatabaseURL

API_V1_STR = "/api"

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30    # one hour
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30 * 10  # one month

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI example application")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = ''
if not MONGODB_URL:
    MONGODB_URL = DatabaseURL(
        f"mongodb+srv://quang:4Y8mat8PewCjmXVe@cluster0.xdxj1.mongodb.net/circleci-test?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE"
    )
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)

database_name = 'circleci-test'
profiles_collection_name = "profiles"
users_collection_name = "users"
images_collection_name = "images"
devices_collection_name = "devices"
authen_tokens_collection_name = "authen_tokens"
