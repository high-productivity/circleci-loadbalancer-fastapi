import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret

API_V1_STR = "/api"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30    # one hour
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30 * 10  # one month

load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI example application")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))
