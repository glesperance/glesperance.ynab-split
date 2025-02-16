from pydantic_settings import BaseSettings, SettingsConfigDict


class SplitwiseClientSettings(BaseSettings):
    consumer_key: str
    consumer_secret: str
    api_key: str

    model_config = SettingsConfigDict(env_prefix="SPLITWISE_")


splitwise_client_settings = SplitwiseClientSettings()