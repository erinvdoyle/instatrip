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
SHEET = GSPREAD_CLIENT.open('Instatrip').sheet1

def greeting():
    """
    Greets the user when the program is run.
    """
    print("Welcome to Instatrip, your booking buddy.")

def get_trip_details():
    """
    Asks user for travel date, flexibility, and length of trip.
    """
    # Get travel date
    travel_date_str = input("First things first, when would you like to depart? (Please enter a date in YYYY-MM-DD format): ")
    
    try:
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d")
    except ValueError:
        print("Oops. Please enter a valid date in YYYY-MM-DD format.")
        return None

    # Get flexibility
    flexibility_response = input("Are you flexible with your date (+/- 1-3 days)? (yes/no): ").strip().lower()
    if flexibility_response not in ['yes', 'no']:
        print("Please answer with 'yes' or 'no'.")
        return None

    # Get length of stay
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

def type_of_trip():
    """
    Determines the occasion for the trip.
    """
    print("Please select the most applicable choice for your trip:")
    options = ["Romantic", "Solo Travel", "Hen Party", "Friends/Fam"]
    
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
    factors = ["Nightlife", "Culture", "Cuisine", "Outdoors", "Shopping", "Off Beaten Path"]
    
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

def rank_cities(sheet, selected_trip_type, selected_factors):
    """
    Ranks cities based on user preferences from Google Sheets, with higher rank being better.
    """
    cities = sheet.get_all_records()  
    
    ranked_cities = []
    
    for city in cities:
        score = 0
        
        
        if city[selected_trip_type] == "1":  
            score += 5  
        
        for factor in selected_factors:
            score += (5 - int(city[factor]))  

        ranked_cities.append((city['Destination'], score))

    
    ranked_cities.sort(key=lambda x: x[1], reverse=True)

    return ranked_cities[:3]  

def rate_importance():
    """
    Collects importance ranking for safety and accessinbility factors from the user.
    """
    factors_to_rate = ["Safety", "Accessibility", "Transportation", "Tourist", "Language Barrier"]
    
    ratings = {}
    
    for factor in factors_to_rate:
        while True:
            try:
                rating = int(input(f"Rate the importance of {factor} (1-5, with 1 being most important): "))
                if 1 <= rating <= 5:
                    ratings[factor] = rating
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    return ratings

def adjust_city_scores(top_cities, ratings):
    """
    Adjusts scores of top cities based on safety and accessibility ratings.
    """
    adjusted_cities = []

    for city_name, score in top_cities:
        adjustment_factor = sum(6 - ratings[factor] for factor in ratings)  
        adjusted_score = score + adjustment_factor
        
        adjusted_cities.append((city_name, adjusted_score))

   
    adjusted_cities.sort(key=lambda x: x[1], reverse=True)

    return adjusted_cities[:3]  


#greeting()
#get_trip_details()
#type_of_trip()
#important_factors()
#rank_cities(SHEET, selected_trip_type, selected_factors)    
