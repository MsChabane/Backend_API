from pydantic_settings import SettingsConfigDict ,BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:str 

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


config = Settings()

