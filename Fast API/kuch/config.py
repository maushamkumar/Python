from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_username: str = Field(validation_alias='MYSQL_USER')
    database_password: str = Field(validation_alias='MYSQL_PASSWORD')
    database_hostname: str = Field(validation_alias='MYSQL_HOST')
    database_port: str = Field(validation_alias='MYSQL_PORT')
    database_name: str = Field(validation_alias='MYSQL_DATABASE')
    secret_key: str = Field(validation_alias='SECRET_KEY')
    algorithm: str = Field(validation_alias='ALGORITHM')
    access_token_expire_minutes: int = Field(validation_alias='ACCESS_TOKEN_EXPIRE_MINUTES')

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
