from pydantic_settings import SettingsConfigDict ,BaseSettings


class Settings(BaseSettings):
    DATABASE_URL : str 
    JWT_SECRET : str
    JWT_ALGORITHME : str
    MAIL_USERNAME : str  
    MAIL_PASSWORD: str 
    MAIL_FROM : str
    MAIL_SERVER:str
    MAIL_PORT:int
    SERILIZER_SECRET:str
    REDIS_URL:str
    ALLOWED_ORIGINS:list
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


config = Settings()

