from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str
    app_description: str
    database_url: str
    database_sync_url: str

    model_config = SettingsConfigDict(
        env_file='backend/.env',
        env_file_encoding="utf-8"
    )

settings = Settings()
