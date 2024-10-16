import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import requests
from ryanair import Ryanair



SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Instatrip').sheet1

airport_codes = {
    "Amsterdam": "AMS",
    "Athens": "ATH",
    "Barcelona": "BCN",
    "Beirut": "BEY",
    "Berlin": "BER",
    "Bratislava": "BTS",
    "Brussels": "BRU",
    "Bucharest": "OTP",
    "Budapest": "BUD",
    "Copenhagen": "CPH",
    "Dubrovnik": "DBV",
    "Helsinki": "HEL",
    "Istanbul": "IST",
    "Tbilisi": "TBS",
    "Larnaka": "LCA",
    "Paphos": "PFO",
    "Lisbon": "LIS",
    "London": "LON",
    "Ljubljana": "LJU",
    "Madrid": "MAD",
    "Minsk": "MSQ",
    "Oslo": "OSL",
    "Paris": "CDG",
    "Podgorica": "TGD",
    "Prague": "PRG",
    "Riga": "RIX",
    "Rome": "FCO",
    "Sofia": "SOF",
    "Stockholm": "ARN",
    "Tallinn": "TLL",
    "Tunis": "TUN",
    "Vienna": "VIE",
    "Vilnius": "VNO",
    "Warsaw": "WAW",
    "Zurich": "ZRH"
}

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

    flexibility_days = 0
    if flexibility_response == 'yes':
        flexibility_days = int(input("How many days of flexibility do you have? (1-3): "))
        if not (1 <= flexibility_days <= 3):
            print("Please enter a number between 1 and 3.")
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
        'flexibility_days': flexibility_days,
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

        if selected_trip_type in city and city[selected_trip_type] == '1':
             score += 5  # Arbitrary score boost

        for factor in selected_factors:
             if factor in city:
                 score += (5 - int(city[factor]))  

        
        if 'Destination' in city:
             ranked_cities.append((city['Destination'].strip(), score))  

     # Sort by score (higher is better)
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

# Library for Ryanair API provided by https://github.com/cohaolain/ryanair-py

from datetime import timedelta
from ryanair import Ryanair

def find_cheapest_flights(top_cities, trip_details):
    """Finds the cheapest flights to each of the top cities using Ryanair API, with Dublin as the default departure city."""
    
    api = Ryanair(currency="EUR")  
    travel_date = trip_details['travel_date']
    length_of_stay = trip_details['length_of_stay']
    
    flights_info = {}

    
    for index, city_name in enumerate(top_cities[:3]):  
        destination_code = airport_codes.get(city_name)

        if not destination_code:
            print(f"Warning: No airport code found for {city_name}. Skipping.")
            continue

        
        outbound_date = travel_date + timedelta(days=index)  
        inbound_date = outbound_date + timedelta(days=length_of_stay)  

        try:
            # Utilize Ryanair API
            flights = api.get_cheapest_return_flights(
                "DUB",  
                outbound_date,  
                outbound_date,  
                inbound_date,   
                inbound_date    
            )

            if flights and len(flights) > 0:
                flight_info = flights[0]  
                flight_price_info = {
                    'flight_number': flight_info.outbound.flightNumber,
                    'price': flight_info.totalPrice,  
                    'currency': flight_info.outbound.currency,  
                    'departure_time': flight_info.outbound.departureTime,
                    'origin': flight_info.outbound.originFull,
                    'destination': flight_info.outbound.destinationFull,
                }

                flights_info[city_name] = flight_price_info

            else:
                flights_info[city_name] = 'No flights found'

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    return flights_info

def main():
    greeting()

    trip_details = get_trip_details()

    if trip_details:
        selected_trip_type = type_of_trip()
        selected_factors = important_factors()

        top_cities_with_scores = rank_cities(SHEET, selected_trip_type, selected_factors)

        print("Top 3 suitable cities:")

        top_cities_names_only = [city[0] for city in top_cities_with_scores]

        for city in top_cities_with_scores:
            print(city[0])

        ratings = rate_importance()
        final_top_cities = adjust_city_scores(top_cities_with_scores, ratings)

        print("\nFinal Top Cities Considering Importance Ratings:")

        for city in final_top_cities:
            print(city[0])

        flights_info = find_cheapest_flights(top_cities_names_only, trip_details)

        print("\nCheapest Flights Information:")

        for city_name, flight in flights_info.items():
            if isinstance(flight, dict):  
                print(f"{city_name}: Flight Number: {flight['flight_number']}, Price: {flight['price']} {flight['currency']}, Departure Time: {flight['departure_time']}")
            else:
                print(f"{city_name}: {flight}")

if __name__ == "__main__":
    main()
