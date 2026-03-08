from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "University Assignment Manager API"
    api_prefix: str = ""
    database_url: str = "sqlite:///./university_assignment_manager.db"
    secret_key: str = "change_this_secret_key_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_sender: str = ""

    upload_dir: str = "uploads/submissions"
    log_level: str = "INFO"
    rate_limit_max_requests: int = 120
    rate_limit_window_seconds: int = 60
    rate_limit_login_max_requests: int = 10
    rate_limit_login_window_seconds: int = 60
    rate_limit_register_max_requests: int = 5
    rate_limit_register_window_seconds: int = 60


settings = Settings()
