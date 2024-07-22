from pydantic_settings import BaseSettings, SettingsConfigDict

from .schema import CategoryGroupName


class YNABClientSettings(BaseSettings):

    base_url: str = "https://api.youneedabudget.com/v1"

    model_config = SettingsConfigDict(
        env_prefix="YNAB_", env_file=".env", arbitrary_types_allowed=True
    )


client_settings = YNABClientSettings()
