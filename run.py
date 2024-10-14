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
        'flexibility': flexibility_response,
        'length_of_stay': length_of_stay
    }

#def get_user_preferences():

def type_of_trip():
    """
    Determines the occasion for the trip.
    """
    print("Please select the most applicable choice for your trip:")
    options = ["romantic", "solo travel", "hen party", "friends and family"]
    
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= len(options):
                selected_trip_type = options[choice - 1]
                print(f"You selected: {selected_trip_type}")
                return selected_trip_type
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def important_factors():
    """
    Collects up to three important factors from the user.
    """
    print("Select up to three important factors (enter numbers separated by commas):")
    factors = ["nightlife", "culture", "cuisine", "outdoors", "shopping", "off the beaten path"]
    
    for i, factor in enumerate(factors, start=1):
        print(f"{i}. {factor}")

    while True:
        choices = input("Enter your choices (e.g., 1,2,3): ").split(',')
        selected_factors = []
        
        for choice in choices:
            try:
                index = int(choice.strip()) - 1
                if 0 <= index < len(factors):
                    selected_factors.append(factors[index])
            except ValueError:
                continue
        
        if len(selected_factors) <= 3:
            print(f"You selected: {selected_factors}")
            return selected_factors
        else:
            print("Please select up to three factors.")



    

greeting()
get_trip_details()
type_of_trip()
important_factors()