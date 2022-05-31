import os


MONGO_USER = os.getenv("MONGO_USER", None)
MONGO_PASS = os.getenv("MONGO_PASS", None)

DB_HOST = os.getenv("DB_HOST", None)
DB_PORT = os.getenv("DB_PORT", None)
DB_NAME = os.getenv("DB_NAME", None)

MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{DB_HOST}:{DB_PORT}/"
