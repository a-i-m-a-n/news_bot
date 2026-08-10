import os
import json
import datetime
from crewai.tools import tool
from google.oauth2 import service_account
from googleapiclient.discovery import build

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _get_sheets_service():
    creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is not set.")
    creds_info = json.loads(creds_json)
    credentials = service_account.Credentials.from_service_account_info(
        creds_info, scopes=_SCOPES
    )
    return build("sheets", "v4", credentials=credentials)


@tool("Sheets Logger Tool")
def log_to_sheet(headline: str, summary: str, source_url: str) -> str:
    """
    Appends a structured news entry (Date, Headline, Summary, Source URL)
    to the configured Google Sheet.

    Args:
        headline: The news headline.
        summary: The short summary text.
        source_url: The article's source URL.
    """
    spreadsheet_id = os.environ.get("GOOGLE_SHEET_ID")
    if not spreadsheet_id:
        return "Error: GOOGLE_SHEET_ID is not set."

    try:
        service = _get_sheets_service()
        row = [[
            datetime.datetime.utcnow().isoformat(),
            headline,
            summary,
            source_url,
        ]]
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A:D",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": row},
        ).execute()
    except Exception as e:
        return f"Error logging to Google Sheets: {e}"

    return "Logged to Google Sheets successfully."
