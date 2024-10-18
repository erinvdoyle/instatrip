import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

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
    travel_date_str = input("First things first, when would you like to depart? (Please enter a date in YYYY-MM-DD format):\n ")

    try:
        travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d")
    except ValueError:
        print("Oops. Please enter a valid date in YYYY-MM-DD format.")
        return None

    flexibility_response = input("Are you flexible with your date (+/- 1-3 days)? (yes/no): \n").strip().lower()
    if flexibility_response not in ['yes', 'no']:
        print("Please answer with 'yes' or 'no'.")
        return None

    flexibility_days = 0
    if flexibility_response == 'yes':
        flexibility_days = int(input("How many days of flexibility do you have? (1-3): \n"))
        if not (1 <= flexibility_days <= 3):
            print("Please enter a number between 1 and 3.")
            return None

    try:
        length_of_stay = int(input("How many days do you plan to stay? \n"))
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
            choice = int(input("Enter the number corresponding to your choice: \n"))
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
        choices = input("Enter your choices (e.g., 1,2,3): \n").split(',')
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

#Ranking tutorial credit: 
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

        if 'City' in city:
             ranked_cities.append((city['City'].strip(), score))

     # Sort by score (higher is better)
    ranked_cities.sort(key=lambda x: x[1], reverse=True)

    return ranked_cities[:3]

def rate_importance():
    """
    Collects importance ranking for safety and accessibility factors from the user.
    """
    factors_to_rate = ["Safety", "Accessibility", "Transportation", "Tourist", "Language Barrier"]

    ratings = {}

    for factor in factors_to_rate:
        while True:
            try:
                rating = int(input(f"Rate the importance of {factor} (1-5, with 1 being most important): \n"))
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

def get_airport_codes(sheet):
    """
    Get airport codes from Google Sheet using 'City' and 'IATA' columns to access airport codes
    """
    records = sheet.get_all_records()
    airport_codes = {}
    for record in records:
        city = record['City'].strip()
        code = record['IATA'].strip()
        airport_codes[city] = code
    return airport_codes

#Credit for help implementing API in this function and find_cheapest_flights(): 
def search_ryanair_flights(origin, destination, outbound_date, adults=1, teens=0, children=0, infants=0):
    """
    Searches flights using Ryanair API (via RapidAPI).
    """
    url = "https://ryanair2.p.rapidapi.com/api/v1/searchFlights"
    querystring = {
        "origin": origin,
        "destination": destination,
        "outboundDate": outbound_date,
        "adults": str(adults),
        "teens": str(teens),
        "children": str(children),
        "infants": str(infants)
    }
    #Credit to Rapid API for Ryanair API key
    headers = {
        "x-rapidapi-host": "ryanair2.p.rapidapi.com",
        "x-rapidapi-key": "1ba388bfffmsh0eff684773db243p19641djsn51bdcd6bec4f"  # Replace with your RapidAPI key
    }

    try:
        logging.debug(f"Sending request to {url} with params {querystring}")
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raises HTTPError for bad responses
        logging.debug(f"Response received: {response.text}")
        return response.json()  # Return JSON data if successful
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        logging.error(f"Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error searching for flights: {req_err}")
    return None

def find_cheapest_flights(sheet, top_cities, trip_details):
    """
    Finds the cheapest flights for a list of top cities using Ryanair API via RapidAPI.
    """
    airport_codes = get_airport_codes(sheet)  
    origin = trip_details['departure_airport']  
    flight_results = []

    for city_name in top_cities:
        destination_code = airport_codes.get(city_name) 

        if destination_code:
            outbound_date = trip_details['departure_date']  
            print(f"Fetching flights for {city_name} (IATA: {destination_code})...")

            # Search flights via RapidAPI Ryanair
            flight_data = search_ryanair_flights(origin, destination_code, outbound_date)

            if flight_data:
                # Parse the response and find the cheapest flight
                cheapest_flight = None
                for trip in flight_data['data']['trips']:
                    for date in trip['dates']:
                        for flight in date['flights']:
                            if not cheapest_flight or flight['regularFare']['fares'][0]['amount'] < cheapest_flight['regularFare']['fares'][0]['amount']:
                                cheapest_flight = flight

                if cheapest_flight:
                    flight_info = {
                        'city': city_name,
                        'flight_number': cheapest_flight['flightNumber'],
                        'price': cheapest_flight['regularFare']['fares'][0]['amount'],
                        'departure_time': cheapest_flight['time'][0],
                        'arrival_time': cheapest_flight['time'][1]
                    }
                    flight_results.append(flight_info)
                else:
                    print(f"No fares found for {city_name}.")
            else:
                print(f"Error fetching flights for {city_name}")
        else:
            print(f"No airport code found for {city_name}")

    return flight_results

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

        trip_details['departure_airport'] = 'DUB'
        trip_details['departure_date'] = trip_details['travel_date'].strftime("%Y-%m-%d")

        flights_info = find_cheapest_flights(SHEET, top_cities_names_only, trip_details)

        print("\nCheapest Flights Information:")
        for flight in flights_info:
            print(f"{flight['city']}: Flight Number: {flight['flight_number']}, Price: {flight['price']} EUR, "
                  f"Departure Time: {flight['departure_time']}, Arrival Time: {flight['arrival_time']}")

if __name__ == "__main__":
    main()
