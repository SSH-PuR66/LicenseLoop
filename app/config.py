from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "dev-secret-change-me"
    database_url: str = "sqlite:///./licenseloop.db"
    app_url: str = "http://localhost:8000"

    stripe_secret_key: str = ""
    stripe_price_id: str = ""
    stripe_webhook_secret: str = ""

    cron_secret: str = "dev-cron-secret"
    free_plan_limit: int = 3

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "reminders@licenseloop.app"

    class Config:
        env_file = ".env"


settings = Settings()
