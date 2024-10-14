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
    #get date
    travel_date_str = input("First things first, when would you like to depart? (Please enter a date in YYYY-MM-DD format, for example: 2025-09-27): ")
    try:
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d")
    except ValueError:
        print("Oops. Please enter a date in YYYY-MM-DD format.")
        return None

    #get flexibility
    flexibility_response = input("Are you flexible with your date (+/- 1-3 days)? (yes/no): ").strip().lower()
    if flexibility_response not in ['yes', 'no']:
        print("Please answer with 'y' for yes or 'n' for no.")
        return None

    #Get length of stay
    try:
        length_of_stay = int(input("How many days do you plan to stay? "))
    except ValueError:
        print("Please enter a valid number for length of stay.")
        return None

    return {
        'travel_date': travel_date,
        'date_flexibility': date_flexibility,
        'length_of_stay': length_of_stay
    }


    

greeting()
get_trip_details()