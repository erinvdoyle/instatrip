import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import random
import time
import emoji
# credit for emoji library: https://pypi.org/project/emoji/
from colorama import Fore, Style, init
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Instatrip').sheet1

def print_colored_background():
    """
    Gets terminal size to create three colored lines the width of the terminal using the coloroma library. Centers the Instatrip tagline within the color block
    """
    terminal_width = os.get_terminal_size().columns
    
    orange_background = "\033[43m"
    reset_style = "\033[0m"
    
    background_line = " " * terminal_width
    
    centered_text = "Europe, but make it spontaneous"
    
    centered_line = centered_text.center(terminal_width)

    print()  
    print(orange_background + background_line + reset_style) 
    print(orange_background + centered_line + reset_style)  
    print(orange_background + background_line + reset_style)  

# Initialize colorama for Windows support
init(autoreset=True)

insta_trip_text = [
    r" ___           _       _____     _       ",
    r"|_ _|_ __  ___| |_ __ |_   _| __(_)_ __  ",
    r" | || '_ \/ __| __/ _` || || '__| | '_ \ ",
    r" | || | | \__ \ || (_| || || |  | | |_) |",
    r"|___|_| |_|___/\__\__,_||_||_|  |_| .__/ ",
    r"                                  |_|    "
]

def colored_instatrip():
    """
    Makes InstaTrip ASCII text tri-colored
    """
    total_lines = len(insta_trip_text)
    top_lines = insta_trip_text[:total_lines // 3]  
    middle_lines = insta_trip_text[total_lines // 3: 2 * total_lines // 3]  
    bottom_lines = insta_trip_text[2 * total_lines // 3:]  

    top_lines = center_text(top_lines)
    middle_lines = center_text(middle_lines)
    bottom_lines = center_text(bottom_lines)

    for line in top_lines:
        print(Fore.YELLOW + line)
    for line in middle_lines:
        print(Fore.LIGHTYELLOW_EX + line)
    for line in bottom_lines:
        print(Fore.RED + line)

menu_text = """
MAIN MENU
---------
1. Start
2. About
3. Exit
"""

def center_text(text):
    """
    Centers the text in the console
    """
    terminal_width = os.get_terminal_size().columns
    centered_lines = [line.center(terminal_width) for line in text]
    return centered_lines


def greeting():
    """
    Greets the user when the program is run.
    """
    print(emoji.emojize(":palm_tree: Welcome to Instatrip, your booking bestie :palm_tree:"))
    time.sleep(3)
    print("First things first. We're going to ask you a few questions about your travel \n dates")
    time.sleep(3)
    print(emoji.emojize("Then we'll get to the fun part: :crystal_ball: Selecting your next trip!"))
    time.sleep(3) 
    print("Grab a suitcase, we're about to get started...")
    time.sleep(3)

def get_trip_details():
    """
    Asks user for travel date, flexibility, and length of trip.
    """
    while True:
        travel_date_str = input(emoji.emojize(":handbag: When would you like to depart? (Please enter a date in YYYY-MM-DD format):\n "))

        try:
            travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d")

            current_date = datetime.now()
            minimum_travel_date = current_date + timedelta(days=1)

            if travel_date < minimum_travel_date:
                print(f"Please enter a date from tomorrow onward (after {minimum_travel_date.date()}).")
                continue  
            
            break
        
        except ValueError:
            print("Oops. Please enter a valid date in YYYY-MM-DD format.")
            return None

    flexibility_response = input(emoji.emojize("Are you flexible with your date (+/- 1-3 days)? (yes/no):person_cartwheeling: \n")).strip().lower()
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
    print(emoji.emojize("Please select the most applicable choice for your trip: :beating_heart: :man_dancing: :chicken:/:deer: :family:"))
    options = ["Romantic Adventure", "Solo Travel", "Hen or Stag Party", "Time with Friends or Family"]

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
    print(emoji.emojize("Select up to three important factors (enter numbers separated by commas): :party_popper: :books: :woman_cook: :mountain:  :shopping_bags:  :magnifying_glass_tilted_left:"))
    factors = ["Nightlife", "History & Culture", "Cuisine", "Outdoorsy Experiences", "Shopping", "Off the Beaten Path Exploration"]

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

    return ranked_cities#[:3]

def select_random_cities(cities, num_cities=3):
    """
    Selects a random sample of cities from a list.
    """
    if len(cities) <= num_cities:
        return cities  
    return random.sample(cities, num_cities)

def generate_new_cities(sheet, selected_trip_type, selected_factors):
    """
    Generates and ranks new cities based on user preferences.
    Safety and accessibility adjustments are applied separately.
    """
    new_top_cities_with_scores = rank_cities(sheet, selected_trip_type, selected_factors)
    new_top_cities = select_random_cities(new_top_cities_with_scores)
    
    print("\nBased on your preferences, here are three new cities:")
    for city in new_top_cities:
        print(city[0])
    
    return new_top_cities


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
    Adjusts scores of top cities based on safety and other factor ratings.
    Only the selected top three cities are adjusted.
    """
    adjusted_cities = []

    for city_name, score in top_cities:
        adjustment_factor = 0

        for factor, rating in ratings.items():
            if factor == 'Safety' or factor == 'Accessibility':
                adjustment_factor += (6 - rating) 

        adjusted_score = score + adjustment_factor
        adjusted_cities.append((city_name, adjusted_score))

    adjusted_cities.sort(key=lambda x: x[1], reverse=True)

    return adjusted_cities


def user_choice_after_ranking(top_cities, sheet, selected_trip_type, selected_factors):
    """
    Prompts the user to choose whether to keep the ranked cities and move forward,
    generate three new cities, or start the program over.
    If they choose to proceed, the program will prompt for safety and accessibility preferences
    """
    while True:
        print("\nAre you happy with these cities?")
        print(emoji.emojize("1. Yes, let's go! :airplane_departure:"))
        print(emoji.emojize("2. No, let's see the next three :man_gesturing_NO:"))
        print(emoji.emojize("3. It's a wash. Start over :wastebasket:"))

        try:
            choice = int(input("Please choose an option (1-3): "))
            if choice == 1:
                print(emoji.emojize("Great! Let's adjust the cities based on your safety and accessibility preferences :service_dog:"))

                user_ratings = rate_importance()

                adjusted_cities = adjust_city_scores(top_cities, user_ratings)

                print("\nHere are your final cities based on safety and accessibility:")
                for city in adjusted_cities:
                    print(f"{city[0]}")

                return adjusted_cities

            elif choice == 2:
                new_top_cities = generate_new_cities(sheet, selected_trip_type, selected_factors)
                return new_top_cities

            elif choice == 3:
                return "start_over"

            else:
                print("Invalid choice. Please select a number from 1 to 3.")
        except ValueError:
            print("Please enter a valid number.")

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

#Credit for help implementing and understanding how to use the API in this function, find_cheapest_flights(), and ask_for_booking(): Mistral AI
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

def ask_for_booking_link(flights_info):
    """
    Asks the user if they would like to generate a booking link for any of the displayed flights and allows user to start over if not
    """
    if not flights_info:
        print("No flight information available.")
        return

    print("Would you like to generate a booking for any of these flights?")
    for idx, flight in enumerate(flights_info, start=1):
        print(f"{idx}. {flight['city']}: Flight Number: {flight['flight_number']}, Price: {flight['price']} EUR")

    print("4. Start over")

    while True:
        try:
            choice = int(input("Please choose an option (1-4): "))
            if 1 <= choice <= len(flights_info):
                selected_flight = flights_info[choice - 1]
                booking_link = f"https://www.ryanair.com/gb/en/booking/home?departureAirport=DUB&arrivalAirport={selected_flight['city']}&outboundDate={trip_details['departure_date']}&adults=1"
                print(f"Booking link for {selected_flight['city']}: {booking_link}")
                break
            elif choice == 4:
                print("Starting over...")
                
                break
            else:
                print("Invalid choice. Please select a number from 1 to 5.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear') 

    colored_instatrip()
    print_colored_background()

    print("\n")
    centered_menu = center_text(menu_text.splitlines())
    for line in centered_menu:
        print(line)
    greeting()

    trip_details = get_trip_details()

    if trip_details:
        selected_trip_type = type_of_trip()
        selected_factors = important_factors()

        all_ranked_cities = rank_cities(SHEET, selected_trip_type, selected_factors)

        initial_top_cities = select_random_cities(all_ranked_cities)

        print("Top suitable cities:")
        for city in initial_top_cities:
            print(city[0])

        while True:
            user_choice = user_choice_after_ranking(initial_top_cities, SHEET, selected_trip_type, selected_factors)

            if user_choice == "start_over":
                main()
                break

            elif user_choice is None:
                new_top_cities = generate_new_cities(SHEET, selected_trip_type, selected_factors)
                initial_top_cities = new_top_cities
                print("\nTop suitable cities:")
                for city in new_top_cities:
                    print(city[0])

                continue

            else:
                final_top_cities = user_choice  # Assign the user choice to final_top_cities

                print(emoji.emojize("\n :party_popper: Let's print your flight information... :party_popper:"))

                # trip_details['departure_airport'] = 'DUB'
                # trip_details['departure_date'] = trip_details['travel_date'].strftime("%Y-%m-%d")
                # flights_info = find_cheapest_flights(SHEET, [city[0] for city in final_top_cities], trip_details)
                # print("\nCheapest Flights Information:")
                # for flight in flights_info:
                #     print(f"{flight['city']}: Flight Number: {flight['flight_number']}, Price: {flight['price']} EUR, "
                #           f"Departure Time: {flight['departure_time']}, Arrival Time: {flight['arrival_time']}")

            #ask_for_booking_link(flights_info)
            break 

if __name__ == "__main__":
    main()
