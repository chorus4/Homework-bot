from os import getenv
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
USE_LOCAL_DB = getenv("USE_LOCAL_DB", "true").lower() in ("true", "1", "yes")


def get_database_url() -> str:
    if USE_LOCAL_DB:
        return "sqlite:///database.db"

    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT", "5432")
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    db = getenv("POSTGRES_DB")

    missing = [
        name
        for name, value in [
            ("POSTGRES_HOST", host),
            ("POSTGRES_USER", user),
            ("POSTGRES_PASSWORD", password),
            ("POSTGRES_DB", db),
        ]
        if not value
    ]
    if missing:
        raise ValueError(
            f"Missing required PostgreSQL environment variables: {', '.join(missing)}"
        )

    return (
        f"postgresql+psycopg://{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}:{port}/{db}"
    )
