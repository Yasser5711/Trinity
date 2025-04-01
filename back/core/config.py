import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://user:password@db/mydatabase")
    APP_NAME = os.getenv("APP_NAME", "FastAPI Application")
    PAYPAL_BASE_URL = os.getenv(
        "PAYPAL_BASE_URL", "https://api.sandbox.paypal.com")
    PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "PAYPAL_CLIENT_ID")
    PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "PAYPAL_SECRET")


settings = Settings()
