import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from .config import client_settings


def get_user_credentials() -> Credentials:
    # Set up the OAuth 2.0 flow
    scope = client_settings.scopes
    flow = InstalledAppFlow.from_client_config(
        client_settings.client_credentials, scope
    )

    # Run the OAuth 2.0 flow to obtain the token
    credentials = flow.run_local_server(port=4000)

    print("------ ADD THIS TO YOUR .ENV FILE ------")
    print(f"GOOGLE_USER_CREDENTIALS={credentials.to_json()}")
    print("-------------------------")

    return credentials


def get_spreadsheet(spreadsheet_name: str) -> gspread.Spreadsheet:
    # Set up the OAuth 2.0 credentials
    scope = client_settings.scopes
    credentials = Credentials.from_authorized_user_info(
        client_settings.user_credentials
    )

    # Authenticate and open the Google Spreadsheet
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open(spreadsheet_name)

    return spreadsheet
