import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Instatrip')

#sales = SHEET.worksheet('sales')

#data = sales.get_all_values()
#print(data)

def greeting():
    """
    Greets the user when program is run
    """
    print("Welcome to Instatrip, your booking buddy")

def get_trip_details():
    """
    Asks user for travel date, flexibility, and length of trip
    """
    travel_date_str = input("First things first, when would you like to depart? (Please enter a date in YYYY-MM-DD format, for example: 2025-09-27): ")
    try:
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d")
    except ValueError:
        print("Oops. Please enter a date in YYYY-MM-DD format.")
        return None

greeting()
get_trip_details()