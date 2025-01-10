from os import getenv

DB_NAME = getenv("DB_NAME", "kinopoisk")
PG_USER = getenv("PG_USER", "postgres")
PG_PASS = getenv("PG_PASS", "qwe123")
PG_HOST = getenv("PG_HOST", "127.0.0.1")
PG_PORT = getenv("PG_PORT", "5432")
