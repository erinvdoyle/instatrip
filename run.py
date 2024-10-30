import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import random
import time
import textwrap
import emoji
from ryanair import Ryanair
from colorama import Fore, Style, init
import os
import platform

# credit for colorama library: https://pypi.org/project/colorama/
# credit for emoji library: https://pypi.org/project/emoji/
# credit for tutorial to clear console:
# https://www.delftstack.com/howto/python/python-clear-console/
# print-multiple-new-lines-to-clear-interpreter-console-in-python

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Instatrip").sheet1

# Start of Starting Screen logic


def print_colored_background():
    """
    Gets terminal size to create three colored lines the width of the
    terminal using the coloroma library. Centers the Instatrip tagline
    within the color block
    """
    # Get the terminal width and create colored lines to display the tagline
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
    r"                                  |_|    ",
]


def colored_instatrip():
    """
    Makes InstaTrip ASCII text tri-colored
    """
    # Split the ASCII text into three sections and
    # display each section in a different color
    total_lines = len(insta_trip_text)
    top_lines = insta_trip_text[: total_lines // 3]
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


def center_text(text):
    """
    Centers the text in the console.
    """
    # Get the terminal width and center the text within the terminal width
    terminal_width = os.get_terminal_size().columns

    # Check if the input is a list
    # (Credit: Mistral AI for help creating a centered text function that
    # works for lists)

    if isinstance(text, list):
        text = "\n".join(text)

    centered_lines = [line.center(
        terminal_width) for line in text.splitlines()]
    return centered_lines


DEFAULT_COLOR = Fore.LIGHTMAGENTA_EX


def print_with_default_color(text):
    """
    Prints text in the default color so that it can be
    applied to the Main Menu List
    """
    print(DEFAULT_COLOR + text + Style.RESET_ALL)


def display_menu():
    """
    Creates a main menu for the starting screen that allows user to choose
    to start the program, read the about, or exit
    """

    # Display the main menu
    menu_text = f"""
{DEFAULT_COLOR}MAIN MENU
{DEFAULT_COLOR}---------
{DEFAULT_COLOR} 1. Start
{DEFAULT_COLOR} 2. About
{DEFAULT_COLOR}3. Exit
{Style.RESET_ALL}"""

    centered_menu = center_text(menu_text)

    for line in centered_menu:
        print(line)

    while True:
        choice = input(Fore.RED + "Please choose an option (1, 2, or 3): ")

        if choice == "1":
            print("\n" * 100)
            os.system("cls" if os.name == "nt" else "clear")
            colored_instatrip()
            greeting()
            break
        elif choice == "2":
            print("\n" * 100)
            os.system("cls" if os.name == "nt" else "clear")
            read_about()
            break
        elif choice == "3":
            print(Fore.YELLOW + "Exiting the program...")
            exit()
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 1, 2, or 3.")


def clear_screen():
    """
    Clears the terminal screen
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


# Greeting Screen


def greeting():
    """
    Greets the user when the program is run.
    """
    # Display a welcome message and instructions for using InstaTrip
    welcome_message = emoji.emojize(
        "\n:palm_tree: "
        + Fore.LIGHTMAGENTA_EX
        + " Welcome to Instatrip, your booking bestie :palm_tree:\n"
    )
    first_message = (
        Fore.YELLOW
        + "First we'll ask you a few questions about your travel dates \n"
    )
    fun_part_message = emoji.emojize(
        Fore.LIGHTMAGENTA_EX
        + "Then we'll get "
        + "to the fun part: :crystal_ball:  Selecting your next trip!\n"
    )
    get_started_message = (
        Fore.YELLOW + "Grab your suitcase, we're about to get started...\n"
    )

    for line in center_text(welcome_message):
        print(line)
        print("")
    time.sleep(2)

    for line in center_text(first_message):
        print(line)
        print("")
    time.sleep(2)

    for line in center_text(fun_part_message):
        print(line)
        print("")
    time.sleep(2)

    for line in center_text(get_started_message):
        print(line)
        print("")
    time.sleep(4)


# About Page


def get_terminal_width():
    """
    Get the current width of the terminal
    """
    return os.get_terminal_size().columns


def wrap_text(text):
    """
    Wraps text to fit within the terminal width
    """
    width = get_terminal_width()
    return textwrap.fill(text, width)

def read_about():
    """
    Displays the about text for both the company and the developer :)
    """
    # Clear the console
    clear_screen()

    # Clear the console using blank lines just in case clear_screen()
    # fails
    print("\n" * 100)

    print(Style.BRIGHT + Fore.MAGENTA + "About InstaTrip" + Style.RESET_ALL)
    print(
        wrap_text(
            Fore.YELLOW
            + "InstaTrip is a travel planning program designed to bring "
            + "spontaneity to the user's next vacation. After asking a "
            + "few simple questions with data compiled by a Google Sheet, "
            + "the program curates a list of personalized European "
            + "destinations. The departure city is currently set to "
            + "Dublin, Ireland, with the aim of expanding departure cities "
            + "in the future"
        )
    )
    print("")
    print(
        wrap_text(
            Fore.YELLOW
            + "For each destination, flight data is retrieved by the "
            + "Ryanair API, showcasing the cheapest available flights. "
            + "The user may then choose to view detailed flight "
            + "information and receive booking instructions"
        )
    )
    print("")
    print(
        wrap_text(
            Fore.LIGHTRED_EX
            + "Disclaimer:"
            + Fore.YELLOW
            + " InstaTrip is a student project and not affiliated "
            + "with Ryanair. Prices + details are updated in real-time "
            + "and subject to change. InstaTrip wishes the user the "
            + "happiest of holidays and cannot be held responsible "
            + "for any travel mishaps or misadventures :)"
        )
    )
    print("")
    print(
            Style.BRIGHT + Fore.MAGENTA + "About the Developer"
            + Style.RESET_ALL)
    print(
    wrap_text(
        Fore.YELLOW
        + "InstaTrip was developed by Erin Doyle, a student "
        + "of Code Institute's Full-Stack Software Development "
        + "program. Her InstaTrip travel preferences are: Romantic "
        + "(her husband vetoed 'Solo Trip') + Culinary, Outdoorsy, "
        + "and Off the Beaten Path.  "
        + Style.BRIGHT + Fore.LIGHTCYAN_EX
        + "https://github.com/erinvdoyle" + Style.NORMAL
    )
)

    print(" ")
    while True:
        choice = input(Fore.RED + "Enter 1 to return to Main Menu: \n")

        if choice == "1":
            os.system("cls" if os.name == "nt" else "clear")
            colored_instatrip()
            print_colored_background()
            display_menu()
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 1")


# Data Collection to Set Flight Parameters for Ryanair API


def get_trip_details():
    """
    Asks user for travel date, flexibility, and length of trip.
    """
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    print("")

    # Inform the user that the departure city is Dublin
    print(
        emoji.emojize(
            Fore.GREEN
            + ":shamrock:" + "  " + "Please note that InstaTrip hails from "
            + "the emerald isle of Ireland, with our \ndeparture city set to "
            + "Dublin. New departure cities take off soon! :shamrock:"
        )
    )
    print(" ")

    # Get the travel date from the user
    while True:
        travel_date_str = input(
            emoji.emojize(
                Style.BRIGHT + Fore.MAGENTA
                + ":handbag:  When would you like to depart? "
                "(Please enter a date in YYYY-MM-DD format): \n"
                + Style.NORMAL
            )
        )

        try:
            # Convert the input string to a datetime object
            travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d")

            # Set the minimum and maximum travel dates
            current_date = datetime.now()
            minimum_travel_date = current_date + timedelta(days=1)
            maximum_travel_date = current_date + timedelta(days=182)

            # Validate the travel date
            if travel_date < minimum_travel_date:
                print(
                    Fore.RED + f"Please enter a date from tomorrow onward "
                    f"(after {minimum_travel_date.date()})."
                )
                continue
            elif travel_date > maximum_travel_date:
                print(
                    Fore.RED + f"Please enter a date no further than six "
                    + "months from today "
                    f"(before {maximum_travel_date.date()})."
                )
                continue

            break

        except ValueError:
            print(
                Fore.RED + "Oops. Please enter a valid date "
                + "in YYYY-MM-DD format."
            )
            continue

    # Get the user's departure date flexibility
    while True:
        flexibility_response = (
            input(
                emoji.emojize(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + "Are you flexible with your departure date "
                    + "(+/- 1-3 days)? "
                    + "(yes/no):person_cartwheeling: \n"
                    + Style.NORMAL
                )
            )
            .strip()
            .lower()
        )
        if flexibility_response not in ["yes", "no"]:
            print(Fore.RED + "Please answer with 'yes' or 'no'.")
        else:
            break

    # If the user is flexible, get the number of flexibility days
    flexibility_days = 0
    if flexibility_response == "yes":
        while True:
            try:
                flexibility_days = int(
                    input(
                        Style.BRIGHT
                        + Fore.MAGENTA
                        + "How many days of departure flexibility do you "
                        + "have? (1-3): \n"
                        + Style.NORMAL
                    )
                )
                if not (1 <= flexibility_days <= 3):
                    print(Fore.RED + "Please enter a number between 1 and 3.")
                else:
                    break
            except ValueError:
                print(
                    Fore.RED + "Please enter a valid number for flexibility "
                    + "days."
                )
                continue

    # Get the length of stay from the user
    while True:
        try:
            length_of_stay = int(
                input(
                    Style.BRIGHT + Fore.MAGENTA
                    + "How many days do you plan to stay? "
                    + "(Enter a minimum of 1 and maximum of 59)\n"
                    + Style.NORMAL
                )
            )
            if not (1 <= length_of_stay <= 59):
                print(Fore.RED + "Please enter a number between 1 and 59.")
            else:
                break
        except ValueError:
            print(Fore.RED + "Please enter a valid number for length of stay.")
            continue

    # Return trip details as a dictionary
    return {
        "travel_date": travel_date,
        "flexibility": flexibility_response,
        "flexibility_days": flexibility_days,
        "length_of_stay": length_of_stay,
    }


# Data Collection of User Preferences to Rank Cities via Google Sheet


def type_of_trip():
    """
    Determines the occasion for the trip.
    """

    # Clear the console
    os.system("cls" if os.name == "nt" else "clear")
    print(" ")

    # Print the trip type selection prompt
    print(
        Style.BRIGHT
        + Fore.MAGENTA
        + "Please select the most applicable choice for your trip: \n"
        + Style.NORMAL
    )

    # Define the trip type options
    options = [
        emoji.emojize("Romantic Adventure :beating_heart:"),
        emoji.emojize("Solo Travel :man_dancing:"),
        emoji.emojize("Hen or Stag Party :tropical_drink:"),
        emoji.emojize("Time with Friends or Family :family:"),
    ]

    # Print the trip type options
    colored_options = [Fore.LIGHTMAGENTA_EX + option for option in options]
    for i, option in enumerate(colored_options, start=1):
        print(Fore.LIGHTMAGENTA_EX + f"{i}. {option}")

    # Get the user's choice
    while True:
        try:
            choice = int(
                input(
                    Style.BRIGHT
                    + Fore.LIGHTMAGENTA_EX
                    + "\nEnter the number corresponding to your choice: \n"
                    + Style.NORMAL
                )
            )
            # Validate the user's choice
            if 1 <= choice <= len(options):
                selected_trip_type = options[choice - 1]
                print(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + f"You selected: {selected_trip_type}"
                    + Style.NORMAL
                )
                print("")
                return selected_trip_type
            else:
                print(
                    Fore.RED + "Invalid choice. Please select "
                    + "a number from the list."
                )
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")


def important_factors():
    """
    Collects up to three important factors from the user.
    """
    # Print the important factors selection prompt
    print(
        Style.BRIGHT
        + Fore.LIGHTCYAN_EX
        + "Select up to three important factors (enter numbers separated "
        "by commas): \n" + Style.NORMAL
    )

    # Define the important factors options
    factors = [
        emoji.emojize("Nightlife :cityscape:"),
        emoji.emojize("History & Culture :books:"),
        emoji.emojize("Cuisine :fork_and_knife:"),
        emoji.emojize("Outdoorsy Experiences :mountain:"),
        emoji.emojize("Shopping :shopping_bags:"),
        emoji.emojize("Off the Beaten Path Exploration :world_map:"),
    ]

    # Print the important factors
    for i, factor in enumerate(factors, start=1):
        print(Fore.LIGHTCYAN_EX + f"{i}. {factor}")

    # Get the user's choices
    while True:
        print("")
        choices = input(
            Style.BRIGHT
            + Fore.LIGHTCYAN_EX
            + "Enter your choices (e.g., 1,2,3): \n"
            + Style.NORMAL
        ).split(",")

        # Check for duplicates in choices
        if len(choices) != len(set(choices)):
            print(Fore.RED + "Duplicate choices are not allowed. Please try again.")
            continue

        selected_factors = []
        invalid_choices = []

        # Validate the user's choices
        for choice in choices:
            try:
                index = int(choice.strip()) - 1
                if 0 <= index < len(factors):
                    if factors[index] not in selected_factors:
                        selected_factors.append(factors[index])
                else:
                    invalid_choices.append(choice.strip())
            except ValueError:
                invalid_choices.append(choice.strip())

        # Handle invalid choices
        if invalid_choices:
            print(
                Fore.RED
                + "Invalid input(s): "
                + ", ".join(invalid_choices)
                + ". Please choose numbers between 1 "
                + "and {}.".format(len(factors))
            )
            continue

        # Handle too many choices
        if len(selected_factors) > 3:
            print(Fore.RED + "Please select up to three factors.")
            continue

        # Handle no choices
        elif len(selected_factors) == 0:
            print(Fore.RED +
                  "You must select at least one factor. Please try again.")
            continue

        # Print selected factors and return
        selected_factors_str = ", ".join(selected_factors)
        print(
            Style.BRIGHT
            + Fore.LIGHTCYAN_EX
            + f"You selected: {selected_factors_str}"
            + Style.NORMAL
        )
        print("")
        print("\n" * 3)
        time.sleep(2)
        clear_screen()
        drumroll()
        return selected_factors


# Logic to Rank Cities from Google Sheet Based on User Preferences
# and Randomly Select Three of them

# Ranking tutorial credit using the sort method:
# https://sparkbyexamples.com/python/sort-using-lambda-in-python/
# "How Do I Create A Scoring System in Python - Stack Overflow":
# https://stackoverflow.com/questions/50115873/how-do-i-create-a-scoring-system-in-python

def rank_cities(sheet, selected_trip_type, selected_factors):
    """
    Ranks cities based on user preferences from Google Sheets,
    with higher rank being better.
    """
    # Get all city data from the Google Sheets worksheet
    cities = sheet.get_all_records()

    ranked_cities = []

    # Iterate through each city and calculate its score based
    # on user preferences
    for city in cities:
        score = 0

        # If the city is suitable for the selected trip type, add 5
        # points to its score
        if selected_trip_type in city and city[selected_trip_type] == "1":
            score += 5

        # For each selected important factor, add points to the city's
        # score based on its rating
        for factor in selected_factors:
            if factor in city:
                score += 5 - int(city[factor])

        # Add the city and its score to the ranked cities list
        if "City" in city:
            ranked_cities.append((city["City"].strip(), score))

    # Sort the ranked cities list by score
    ranked_cities.sort(key=lambda x: x[1], reverse=True)

    return ranked_cities  # [:3]

# Random Tutorial Credit: https://www.w3schools.com/python/module_random.asp


def select_random_cities(cities, num_cities=3):
    """
    Selects a random sample of cities from a list.
    """

    # If the number of cities is less than or equal to the desired sample size
    #  return the entire list
    if len(cities) <= num_cities:
        return cities
    # Otherwise, return a random sample of the desired size
    return random.sample(cities, num_cities)


def drumroll():
    """
    Clears the screen and displays a drumroll message with drum emojis.
    """
    os.system("cls" if os.name == "nt" else "clear")
    # Clear the console
    # clear_screen()

    # Clear the console using blank lines just in case clear_screen()
    # fails
    # print("\n" * 100)

    # Print the drumroll message
    print(
        Style.BRIGHT
        + Fore.RED
        + "Based on your preferences, your top city selections are..."
        + Style.NORMAL
    )
    print("")
    print(Style.BRIGHT + Fore.RED + "drumroll please..." + Style.NORMAL)
    print("")
    time.sleep(2)

    # Print drum emojis
    drum_emojis = emoji.emojize(":drum:  ")
    for _ in range(1):
        print(drum_emojis * 5)
        time.sleep(2)


def generate_new_cities(sheet, selected_trip_type, selected_factors):
    """
    Generates and ranks a list of new cities based on the same user preferences
    """
    # Rank cities based on user preferences
    new_top_cities_with_scores = rank_cities(
        sheet, selected_trip_type, selected_factors
    )
    # Select a random sample of cities from the ranked list
    new_top_cities = select_random_cities(new_top_cities_with_scores)

    # Clear the console
    clear_screen()

    # Clear the console using blank lines just in case clear_screen()
    # fails
    print("\n" * 100)

    # Print the new cities
    print(
        Style.BRIGHT
        + Fore.LIGHTCYAN_EX
        + "\nBased on your preferences, here are three new cities:"
        + Style.NORMAL
    )
    for city in new_top_cities:
        print(emoji.emojize(Fore.LIGHTCYAN_EX + ":star: " + " " + city[0]))

    return new_top_cities


# Logic to Weigh The User's Safety and Accessibility Preferences
# Against the Selected Cities And Order Accordingly

def rate_importance():
    """
    Collects importance ranking for safety and accessibility factors
    from the user.
    """
    factors_to_rate = [
        "Overall Safety",
        "Accessibility",
        "Public Transportation",
        "Tourism-Friendliness",
        "English-Speaking",
    ]

    ratings = {}

    # Get the user's rating for each factor
    for factor in factors_to_rate:
        while True:
            try:
                rating = input(
                    Style.BRIGHT + Fore.MAGENTA + f"Rate the importance of {factor} "
                    "(1-5, with 1 being most important): \n" + Style.NORMAL
                ).strip()

                # Validate the user's input
                if rating == "":
                    print(
                        Fore.RED + "You didn't enter anything. Please "
                        + "enter a number "
                        "between 1 and 5."
                    )
                    continue

                rating = int(rating)

                if 1 <= rating <= 5:
                    ratings[factor] = rating
                    break
                else:
                    print(Fore.RED + "Please enter a number between 1 and 5.")

            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number.")

    return ratings


def adjust_city_scores(top_cities, ratings):
    """
    Adjusts scores of top cities based on safety and other factor ratings.
    Only the selected top three cities are adjusted.
    """
    adjusted_cities = []

    # Adjust the score of each city based on the user's ratings
    for city_name, score in top_cities:
        adjustment_factor = 0

        for factor, rating in ratings.items():
            if factor == "Safety" or factor == "Accessibility":
                adjustment_factor += 6 - rating

        adjusted_score = score + adjustment_factor
        adjusted_cities.append((city_name, adjusted_score))

    # Sort the adjusted cities list by score in descending order
    adjusted_cities.sort(key=lambda x: x[1], reverse=True)

    return adjusted_cities


def user_choice_after_ranking(
    top_cities, sheet, selected_trip_type, selected_factors, city_history=None
):
    """
    Prompts the user to choose whether to keep the ranked cities,
    generate new cities, start over, or return to previous cities.
    If they choose to proceed, the program will prompt for safety and
    accessibility preferences.
    """
    if city_history is None:
        city_history = []

    while True:
        # Print the user's options
        print(
            Style.BRIGHT
            + Fore.LIGHTCYAN_EX
            + "\nAre you happy with these cities?"
            + Style.NORMAL
        )
        print("")
        print(
            emoji.emojize(Fore.LIGHTCYAN_EX + "1. Yes, let's "
                          + "go! :airplane_departure:")
        )
        print(
            emoji.emojize(
                Fore.LIGHTCYAN_EX
                + "2. No, let's see another three cities :cross_mark:"
            )
        )
        print(
            emoji.emojize(
                Fore.LIGHTCYAN_EX + "3. It's a wash. Start over :wastebasket:"
            )
        )

        if city_history:
            print(
                emoji.emojize(
                    Fore.LIGHTCYAN_EX + "4. Return to previous cities "
                    + ":left_arrow:"
                )
            )

        try:
            choice = int(
                input(
                    Style.BRIGHT
                    + Fore.LIGHTCYAN_EX
                    + "\nPlease choose an option: "
                    + Style.NORMAL
                )
            )

            # Handle the user's choice
            if choice == 1:
                os.system("cls" if os.name == "nt" else "clear")
                print("\n" * 1)
                print("")

                print(
                    emoji.emojize(
                        Style.BRIGHT
                        + Fore.MAGENTA
                        + "Great! Let's adjust the cities based on your "
                        + "safety and accessibility \npreferences "
                        + ":service_dog: \n" + Style.NORMAL
                    )
                )

                user_ratings = rate_importance()

                adjusted_cities = adjust_city_scores(top_cities, user_ratings)

                os.system("cls" if os.name == "nt" else "clear")
                print(
                    Style.BRIGHT
                    + Fore.LIGHTCYAN_EX
                    + "\nHere are your final cities ranked by your safety "
                    "and accessibility preferences:" + Style.NORMAL
                )
                for city in adjusted_cities:
                    print(emoji.emojize(Fore.LIGHTCYAN_EX + f":star:  {city[0]}"))

                return adjusted_cities

            elif choice == 2:
                os.system("cls" if os.name == "nt" else "clear")

                city_history.append(top_cities)

                new_top_cities = generate_new_cities(
                    sheet, selected_trip_type, selected_factors
                )
                top_cities = new_top_cities

            elif choice == 3:
                os.system("cls" if os.name == "nt" else "clear")
                return "start_over"

            elif choice == 4 and city_history:
                os.system("cls" if os.name == "nt" else "clear")

                top_cities = city_history.pop()

                print(
                    Style.BRIGHT
                    + Fore.LIGHTCYAN_EX
                    + "\nReturning to your previous cities:"
                    + Style.NORMAL
                )
                for city in top_cities:
                    print(emoji.emojize(Fore.LIGHTCYAN_EX + f":star:  {city[0]}"))

            else:
                print(
                    Fore.RED + "Invalid choice. Please select a valid number")

        except ValueError:
            print(Fore.RED + "Please enter a valid number")


# Logic to Pull Airport Codes of Final City Selections from Google Sheet
# and Pass Them to Ryanair API

def get_airport_codes(sheet):
    """
    Get airport codes from Google Sheet using 'City' and 'IATA' columns
    to access airport codes
    """

    # Get all records from the Google Sheets worksheet
    records = sheet.get_all_records()
    airport_codes = {}
    # Iterate through each record and add the city and airport code
    # to the dictionary
    for record in records:
        city = record["City"].strip()
        code = record["IATA"].strip()
        airport_codes[city] = code
    return airport_codes


# Credit for help implementing and understanding how to use the API
# in this function, find_cheapest_flights(), and ask_for_flight_info():
# Mistral AI

def search_ryanair_flights(
    origin, destination, outbound_date, adults=1,
    teens=0, children=0, infants=0
):
    """
    Searches flights using Ryanair API (via RapidAPI).
    """
    # Define the API endpoint and query parameters
    url = "https://ryanair2.p.rapidapi.com/api/v1/searchFlights"
    querystring = {
        "origin": origin,
        "destination": destination,
        "outboundDate": outbound_date,
        "adults": str(adults),
        "teens": str(teens),
        "children": str(children),
        "infants": str(infants),
    }

    # Credit to Rapid API for Ryanair API key
    # Define the API headers
    headers = {
        "x-rapidapi-host": "ryanair2.p.rapidapi.com",
        "x-rapidapi-key": "1ba388bfffmsh0eff684773db243p19641djsn51bdcd6bec4f",
    }

    try:
        # Send the API request and handle any errors
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


# Logic to Find the Cheapest Flights Among Those Eligible and Ask User
# If They Want to Generate Ryanair Flight Details


def find_cheapest_flights(sheet, top_cities, trip_details):
    """
    Finds the cheapest flights for a list of top cities using Ryanair API
    via RapidAPI.
    """
    # Get the airport codes for the top cities
    airport_codes = get_airport_codes(sheet)
    origin = trip_details["departure_airport"]
    flight_results = []

    # Iterate through each top city and search for flights
    for city_name in top_cities:
        destination_code = airport_codes.get(city_name)

        if destination_code:
            outbound_date = trip_details["departure_date"]
            print(
                Style.BRIGHT
                + Fore.LIGHTCYAN_EX
                + f"Fetching flights for {city_name} (IATA: {destination_code})..."
                + Style.NORMAL
            )

            # Search for flights using the Ryanair API
            flight_data = search_ryanair_flights(
                origin, destination_code, outbound_date
            )

            # Search for flights using the Ryanair API
            if flight_data and "data" in flight_data and "trips" in flight_data["data"]:
                cheapest_flight = None
                for trip in flight_data["data"]["trips"]:
                    for date in trip["dates"]:
                       for flight in date["flights"]:
                            if "regularFare" in flight:
                                if (
                                    not cheapest_flight
                                    or flight["regularFare"]["fares"][0]["amount"]
                                    < cheapest_flight["regularFare"]["fares"][0]["amount"]
                                ):
                                    cheapest_flight = flight
                # Add the flight information to the results list
                if cheapest_flight:
                    flight_info = {
                        "city": city_name,
                        "flight_number": cheapest_flight["flightNumber"],
                        "price": cheapest_flight["regularFare"]["fares"][0]["amount"],
                        "departure_time": cheapest_flight["time"][0],
                        "arrival_time": cheapest_flight["time"][1],
                    }
                    flight_results.append(flight_info)
                else:
                    print(
                        Style.BRIGHT
                        + Fore.LIGHTCYAN_EX
                        + f"No fares found for {city_name}."
                        + Style.NORMAL
                    )
            else:
                print(
                    Style.BRIGHT
                    + Fore.LIGHTCYAN_EX
                    + f"Error fetching flights for {city_name}"
                    + Style.NORMAL
                )
        else:
            print(
                Style.BRIGHT
                + Fore.LIGHTCYAN_EX
                + f"No airport code found for {city_name}"
                + Style.NORMAL
            )

    return flight_results


def ask_for_flight_info(flights_info, trip_details):
    """
    Asks the user if they would like to generate full flight information
    for any of the displayed flights and allows user to start over if not.
    """
    # If there is no flight information available, print a message and
    # return False
    if not flights_info:
        print(
            Style.BRIGHT
            + Fore.MAGENTA
            + "No flight information available."
            + Style.NORMAL
        )
        return False

    # Print the flight information and ask the user if they want to see
    # more details
    print(
        Style.BRIGHT
        + Fore.MAGENTA
        + "Would you like to see booking instructions for any of "
        + "these flights?"
        + Style.NORMAL
    )
    for idx, flight in enumerate(flights_info, start=1):
        print(
            Style.BRIGHT + Fore.CYAN + f"{idx}. {flight['city']}: Flight Number: "
            f"{flight['flight_number']}, Price: {flight['price']} EUR" + Style.NORMAL
        )

    print(Style.BRIGHT + Fore.CYAN + "4. See booking "
          + "instructions for all cities"
          + Style.NORMAL)
    print(Style.BRIGHT + Fore.MAGENTA + "5. Start over" + Style.NORMAL)
    print(" ")
    print(Fore.YELLOW
          + "Please note: Occasionally, booking information may be "
          + "unavailable at the time of your \nrequest, and InstaTrip will be "
          + "unable to provide booking instructions for that city."
          )

    # Get the user's choice and handle any errors
    while True:
        try:
            choice = int(
                input(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + "Please choose an option (1-5): "
                    + Style.NORMAL
                )
            )
            # If the user chooses a flight, display the flight details and
            # ask if they want to restart the program
            if 1 <= choice <= len(flights_info):
                selected_flight = flights_info[choice - 1]
                os.system("cls" if os.name == "nt" else "clear")
                print(" ")
                clear_screen()
                print("\n" * 10)
                print(
                    Style.BRIGHT
                    + Fore.YELLOW
                    + "Flight Details:"
                    + Style.NORMAL
                )
                print(" ")
                print(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + f"City: {selected_flight['city']}"
                    + Style.NORMAL
                )
                print(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + f"Flight Number: {selected_flight['flight_number']}"
                    + Style.NORMAL
                )
                print(
                    Fore.YELLOW
                    + f"Departure Date: {trip_details['departure_date']}"
                    + Style.NORMAL
                )
                print(
                    Fore.YELLOW
                    + f"Departure Time: {selected_flight['departure_time']}"
                    + Style.NORMAL
                )
                print(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + f"Arrival Time: {selected_flight['arrival_time']}"
                    + Style.NORMAL
                )
                print(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + f"Price: {selected_flight['price']} EUR"
                    + Style.NORMAL
                )
                print(" ")
                print(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + "Navigate to www.ryanair.com and enter the city "
                    + "and departure date to secure the best price for "
                    + "your trip to "
                    + emoji.emojize(
                        f":sun_with_face:  {selected_flight['city']} "
                        + ":sun_with_face:")
                    + Style.NORMAL
                )
                print(" ")
                print(
                      Style.BRIGHT + Fore.YELLOW +
                      f"Bon Voyage! {emoji.emojize(':airplane_departure:')}" +
                      Style.NORMAL
                    )

                while True:
                    restart_choice = input(
                        Style.BRIGHT + Fore.MAGENTA +
                        "\nPress Enter to return to Main Menu or type 'all' "
                        + "to see booking instructions for all cities: "
                        + Style.NORMAL
                    )
                    if restart_choice == "":
                        return True  # Return True to indicate that the program
                        # should restart
                    elif restart_choice.lower() == "all":
                        os.system("cls" if os.name == "nt" else "clear")
                        print(" ")
                        print(
                            Style.BRIGHT
                            + Fore.YELLOW
                            + "Flight Details:"
                            + Style.NORMAL
                        )
                        print(" ")
                        for flight in flights_info:
                            print(
                                Style.BRIGHT
                                + Fore.MAGENTA
                                + f"City: {flight['city']}"
                                + Style.NORMAL
                            )
                            print(
                                Style.BRIGHT
                                + Fore.MAGENTA
                                + f"Flight Number: {flight['flight_number']}"
                                + Style.NORMAL
                            )
                            print(
                                Fore.YELLOW
                                + f"Departure Date: {trip_details['departure_date']}"
                                + Style.NORMAL
                            )
                            print(
                                Fore.YELLOW
                                + f"Departure Time: {flight['departure_time']}"
                                + Style.NORMAL
                            )
                            print(
                                Style.BRIGHT
                                + Fore.MAGENTA
                                + f"Arrival Time: {flight['arrival_time']}"
                                + Style.NORMAL
                            )
                            print(
                                Style.BRIGHT
                                + Fore.MAGENTA
                                + f"Price: {flight['price']} EUR"
                                + Style.NORMAL
                            )
                            print(" ")

                        print(" ")
                        print(
                            Style.BRIGHT
                            + Fore.MAGENTA
                            + "Navigate to www.ryanair.com and enter the city "
                            + "and departure date to secure the best price "
                            + "for your trip"
                            + Style.NORMAL
                        )
                        print(" ")
                        print(
                            Style.BRIGHT + Fore.YELLOW +
                            "Bon Voyage! " +
                             Style.NORMAL
                        )

                        while True:
                            restart_choice = input(
                                Style.BRIGHT + Fore.MAGENTA + "\nPress Enter "
                                + "to return to Main Menu "
                                + Style.NORMAL
                            )
                            if restart_choice == "":
                                return True  # Return True to indicate that
                                # the program should restart
                            else:
                                print(Fore.RED + "Invalid input. Please press "
                                      + "Enter to return to Main Menu")
                    else:
                        print(Fore.RED + "Invalid input. Please press Enter "
                              + "to return to Main Menu "
                              + "or type 'all' to see booking instructions "
                              + "for all cities")

            # If the user chooses to see flight information for all three
            # cities, display
            # the flight details for each city
            elif choice == 4:
                os.system("cls" if os.name == "nt" else "clear")
                print(" ")
                print(
                    Style.BRIGHT
                    + Fore.YELLOW
                    + "Flight Details:"
                    + Style.NORMAL
                )
                print(" ")
                for flight in flights_info:
                    print(
                        Style.BRIGHT
                        + Fore.MAGENTA
                        + f"City: {flight['city']}"
                        + Style.NORMAL
                    )
                    print(
                        Style.BRIGHT
                        + Fore.MAGENTA
                        + f"Flight Number: {flight['flight_number']}"
                        + Style.NORMAL
                    )
                    print(
                        Fore.YELLOW
                        + f"Departure Date: {trip_details['departure_date']}"
                        + Style.NORMAL
                    )
                    print(
                        Fore.YELLOW
                        + f"Departure Time: {flight['departure_time']}"
                        + Style.NORMAL
                    )
                    print(
                        Style.BRIGHT
                        + Fore.MAGENTA
                        + f"Arrival Time: {flight['arrival_time']}"
                        + Style.NORMAL
                    )
                    print(
                        Style.BRIGHT
                        + Fore.MAGENTA
                        + f"Price: {flight['price']} EUR"
                        + Style.NORMAL
                    )
                    print(" ")

                print(" ")
                print(
                    Style.BRIGHT
                    + Fore.MAGENTA
                    + "Navigate to www.ryanair.com and enter the city "
                    + "and departure date to secure the best price for "
                    + "your trip"
                    + Style.NORMAL
                )
                print(" ")
                print(Style.BRIGHT + Fore.YELLOW + f"Bon "
                      + "Voyage!  {emoji.emojize(':airplane_departure:')}" +
                      Style.NORMAL)

                while True:
                    restart_choice = input(
                        Style.BRIGHT + Fore.MAGENTA + "\nPress Enter to "
                        + "return to Main Menu "
                        + Style.NORMAL
                    )
                    if restart_choice == "":
                        return True  # Return True to indicate that the
                        # program should restart
                    else:
                        print(Fore.RED + "Invalid input. Please press "
                              + "Enter to return to Main Menu")

            # If the user chooses to start over, print a message and return
            # True
            elif choice == 5:
                print(
                    Style.BRIGHT + Fore.MAGENTA + "Returning to Main "
                    + "Menu..." + Style.NORMAL
                )
                time.sleep(2)
                return True

            # If the user enters an invalid choice, print an error message
            else:
                print(Fore.RED + "Invalid choice. Please select a number "
                      + "from 1 to 5.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")

    return False


def exit():
    """
    Brings the user to the exit art screen and displays a staycation link.
    """
    # Clear the screen and print the exit art and staycation link
    # Clear the console using blank lines
    print("\n" * 50)

    os.system("cls" if os.name == "nt" else "clear")
    print("")
    print("")
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "Bon Voyage!" + Style.NORMAL)
    print("")

    goodbye_art = [
        (f"{Style.BRIGHT + Fore.MAGENTA}              |"),
        (f"{Style.BRIGHT + Fore.MAGENTA}        \\ _ /"),
        (f"{Style.BRIGHT + Fore.MAGENTA}      -= (_) =-"),
        (f"{Style.BRIGHT + Fore.MAGENTA}        /   \\         _\\/\\_"),
        (f"{Style.BRIGHT + Fore.MAGENTA}          |           //o\\  _\\/\\_"),
        (f"{Style.BRIGHT + Fore.YELLOW}   _____ _ __ __ ____ _ | __/o\\\\ _"),
        (f"{Style.BRIGHT + Fore.LIGHTCYAN_EX} =-=-_-__=_-= _=_=-=_,-"
            f"\'|\"\"\"\"-|-,_"),
        (f"{Style.BRIGHT + Fore.LIGHTCYAN_EX}  =- _=-=- -_=-=_,-\"          "
            + "|"),
        (f"{Style.BRIGHT + Fore.LIGHTCYAN_EX} =- =- -=.--"),
    ]

    for line in goodbye_art:
        print(line)

    url = "https://www.lonelyplanet.com/articles/how-to-plan-a-staycation"

    print(" ")
    print(" ")
    time.sleep(2)
    print(
        Style.BRIGHT + Fore.MAGENTA + "Not able to travel at the "
        + "moment?" + Style.NORMAL
    )
    time.sleep(2)
    print(
        Style.BRIGHT + Fore.MAGENTA + emoji.emojize(
            ":house_with_garden:  Perhaps a staycation is in "
            + "order... :house_with_garden:") + Style.NORMAL
    )
    time.sleep(2)
    print(" ")
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX + url + Style.NORMAL)
    print(Style.BRIGHT + Fore.LIGHTCYAN_EX
          + "(Type the url into your browser to get cozy staycation "
          + "tips!)" + Style.NORMAL)
    print(" ")

    # Wait for the user to press Enter to return to the main menu
    while True:
        user_input = input(
            Style.BRIGHT
            + Fore.MAGENTA
            + "Press Enter to return to the main menu: "
            + Style.NORMAL
        )
        if user_input == "":
            # Clear the screen before returning to main menu
            clear_screen()
            break
        else:
            print(
                Fore.RED + "Invalid input! Please press Enter "
                + "to return to the main menu." + Style.NORMAL
            )

    # Clear the screen and restart the program
    clear_screen()
    print("\n")
    colored_instatrip()
    print_colored_background()
    display_menu()


# Logic to Run The Program


def main():
    """
    The main operating function which runs the program
    """
    def initialize_program():
        # Clear the screen and display the InstaTrip logo and menu
        os.system("cls" if os.name == "nt" else "clear")
        print("\n")
        colored_instatrip()
        print_colored_background()
        display_menu()

    while True:
        # Initialize the program and display the menu
        initialize_program()

        # Get the trip details from the user
        trip_details = get_trip_details()
        if not trip_details:
            continue

        # Clear the screen and get the trip type and important factors
        # from the user
        os.system("cls" if os.name == "nt" else "clear")
        selected_trip_type = type_of_trip()
        
        selected_factors = important_factors()

        while True:
            # Rank and select the top cities based on the user's preferences
            all_ranked_cities = rank_cities(SHEET, selected_trip_type, selected_factors)
            initial_top_cities = select_random_cities(all_ranked_cities)

            # Clear the console
            clear_screen()

            # Clear the console using blank lines just in case clear_screen()
            # fails
            # print("\n" * 100)

            print(Style.BRIGHT + Fore.MAGENTA + "Your Curated Destinations:" + Style.NORMAL)
            print("")
            for city in initial_top_cities:
                print(emoji.emojize(Style.BRIGHT + Fore.MAGENTA + ":star: " + " " + city[0] 
                + Style.NORMAL))

            # Ask the user if they are happy with the top cities and
            # get their choice
            user_choice = user_choice_after_ranking(
                initial_top_cities, SHEET, selected_trip_type, selected_factors
            )

            # If the user chooses to start over, clear the screen and
            # restart the program
            if user_choice == "start_over":
                os.system("cls" if os.name == "nt" else "clear")
                print(
                    Style.BRIGHT + Fore.MAGENTA + "Starting "
                    + "over..." + Style.NORMAL
                )
                time.sleep(1)
                break

            # If the user chooses to proceed with the top cities, display
            # the flight information
            elif user_choice is not None:
                final_top_cities = user_choice
                print(" ")
                print(
                    emoji.emojize(
                        Style.BRIGHT
                        + Fore.MAGENTA
                        + "\n :party_popper:  Let's print your flight "
                        "information... :party_popper:" + Style.NORMAL
                    )
                )

                # Set the departure airport and date for the trip details
                trip_details['departure_airport'] = 'DUB'
                travel_date = trip_details.get('travel_date')
                if isinstance(travel_date, list) and travel_date:
                    trip_details['departure_date'] = travel_date[0].strftime("%Y-%m-%d")
                else:
                    trip_details['departure_date'] = (
                        travel_date.strftime("%Y-%m-%d")
                    )

                # Find the cheapest flights for the top cities
                flights_info = find_cheapest_flights(
                    SHEET,
                    [city[0] for city in final_top_cities],
                    trip_details
                )

                # Clear the screen and display the flight information
                os.system("cls" if os.name == "nt" else "clear")
                clear_screen()
                print("\n" * 100)


                print(Style.BRIGHT + Fore.MAGENTA + "\nCheapest Flights "
                      + "Information:" + Style.NORMAL)
                print(" ")
                for flight in flights_info:
                    print(
                        Style.BRIGHT + Fore.LIGHTCYAN_EX
                        + f"{emoji.emojize(':airplane_departure:')}  "
                        + f"{flight['city']}  "
                        + f"{emoji.emojize(':airplane_departure:')} \n"
                        + f"Flight Number: {flight['flight_number']},\n"
                        + f"Price: {flight['price']} EUR\n"
                        + Style.NORMAL
                        )

                # Ask the user if they want to see more flight information
                if ask_for_flight_info(flights_info, trip_details):
                    break


if __name__ == "__main__":
    main()