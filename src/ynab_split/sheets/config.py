from pydantic_settings import BaseSettings, SettingsConfigDict


class GoogleClientSettings(BaseSettings):
    client_credentials: dict
    user_credentials: dict

    scopes: list[str] = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    model_config = SettingsConfigDict(env_prefix="GOOGLE_", env_file=".env")


class GoogleSheetSettings(BaseSettings):
    spreadsheet_name: str
    sheet_name: str

    model_config = SettingsConfigDict(env_prefix="GOOGLE_SHEETS_")


client_settings = GoogleClientSettings()
