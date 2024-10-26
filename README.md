# :sunny: **InstaTrip** :sunny:
## *For When You Want to Travel, But Decision-Making Isn’t Your Thing* 

<p align="center">
  <img src="assets/documentation/landing.png">
</p>

[Visit the deployed site](https://instatrip-ffc10cb98741.herokuapp.com/)

# **Introduction**

Crave the magic of adventure but need the security of cold, hard data? Welcome to **InstaTrip**, your source for perfectly planned travel spontaneity (courtesy of a Google Sheet)

InstaTrip asks you a few simple questions (nothing too deep), then compiles a hand-picked list of European destinations based on your preferences. Fancy a quick solo trip to Bucharest? A hen party in Amsterdam? Maybe a spicy weekend for two in Istanbul? We’ve got you covered. We'll match the occasion of your trip to your chosen interests. Shopping? *Check.* Dining? *Absolutely.* Nightlife? *Cheers!*

But that's not all, reader. **InstaTrip** even saves you the trouble of flight searching. Thanks to the Ryanair API, we’ll show you the cheapest ticket to your destination. Decision fatigue is real, so help us help you. No need to spend hours searching for flights-- that's time better spent agonizing over how to fit your entire wardrobe + toiletries into a 40cm x 20cm bag :fearful:

Don't forget your passport!

# **Table of Contents**
- [Project](#project)
  - [How to Use InstaTrip](#how-to-use-instatrip)
  - [Target Audience](#target-audience)
  - [User Stories](#user-stories)
  - [Site Owner's Goal](#site-owners-goal)
  - [Features to Achieve the goals](#features-to-achieve-the-goals)
- [User Experience](#user-experience)
  - [Program Structure](#program-structure)
  - [Flowchart](#flowchart)
  - [Database Structure](#database-structure)
      - [Google Sheet](#google-sheet)
      - [Ryanair API](#ryanair-api)
  - [Logic Flow](#logic-flow)
  - [Design Choices](#design-choices)
- [Features](#features)
- [Future Features](#future-features)
- [Technologies](#technologies)
  - [Languages](#languages)
  - [Libraries, Programs, and Tools](#libraries-programs-and-tools)
- [Testing](#testing)
  - [Code Validation](#code-validation)
  - [Feature Testing](#feature-testing)
  - [Additional Testing](#additional-testing)
  - [Bugs](#bugs)
- [Deployment](#deployment)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)


# Project 

This program was created for Portfolio Project #3 (Python Essentials) for The Code Institute Full Stack Software Developer program

## How to Use InstaTrip

1. Navigate to `https://instatrip-ffc10cb98741.herokuapp.com`or [follow this link](https://instatrip-ffc10cb98741.herokuapp.com/)
2. Click the *Run Program* button at the top of the page
3. Follow the instructions on the main menu to either read *About* the program or *Start* it
4. After starting the program, answer the questions and select your vacation preferences. Then choose from the cities presented and receive the cheapest flight for your preferred destination. You may then copy the provided link and purchase the flight from Ryanair, *Start Over* to select new cities, or *Exit* the program

## Target Audience

**InstaTrip** is intended for adults (and young people with parental supervision) of all walks of life, based in Ireland and/or within reasonable travelling distance to Dublin airport-- people who would like to explore spontaneous European travel. 

This program is designed to inspire joy. From the colors to the playful tone, whether the user is landlocked or ready for takeoff, **InstaTrip**  is for anyone who'd like a change of pace as it encourages the feelings of excitement and anticipation that accompany planning a big trip. It's to be used as inspiration, for fun, or to plot the next great escape from daily routine :sparkles:

## User Stories
   <details>
   <summary>User Stories for Instatrip (click)</summary>
   
 - **As a new visitor**, I want:
    - A simple and easily understood main menu for hassle-free navigation 
    - A step by step, methodical process that helps me choose the best destination to suit my needs
    - An intuitive process that communicates each step along the way to selecting my next vacation
    - The ability to choose the departure date that fits my schedule
    - A flexible departure date so that I can find the cheapest flights available to me
    - A suggested list of cities to visit tailored to my own preferences
    - A suggested list of cities best suited for my personal occasion
    - Ideas on where to visit based on my travel interests
    - The option to ask for a new selection of cities or return to my previously suggested destinations
    - The flexibility to easily start again if I haven't been offered cities that interest me
    - Destination recommendations that take into account my travel safety and accessibility preferences
    - To be offered the most economical flight choices that fit my needs
    - Real-time flight information with an accurate reflection of prices, flight numbers, and departure times
    - The information needed to book my flight
    - To be able to read about the service
    - To be able to start over or exit the program once my flight information has been generated

 - **As a returning visitor**, I want:
    - A quick and reliable city selection process
    - A variety of cities so that my city suggestions vary based on my preferences
    - The opportunity to receive suggestions for cities I may never have thought about
    - To understand that certain cities I may not have considered are actually tailored to my preferences
    - To be able to generate new cities based on changing travel dates, flexibility, preferences, and trip occasions
    - To receive the best prices and most suitable flights regardless of my varying selections
    </details>

## Site Owner's Goal
   <details>
   <summary>Site Owner's Goal (click)</summary>

  - **As the owner of the site**, I want:
    - To deliver a clean, well-planned interface that seamlessly collects user preferences to predict a tailored selection of vacation destinations
    - To connect my users with the best prices for their chosen destinations and with a reputable airline, Ryanair
    - To offer a variety of choice and a fun factor that encourages repeat vists
    </details>

## Features to Achieve the Goals

<details>
   <summary>Features to Achieve the Goals (click)</summary>

    - The starting screen of the application features a simple main menu for easy navigation
    - The user is walked through the process of entering their departure details and choosing their vacation preferences; every step is explained along the way
    - The tone of the copy and the color and decorative choices for the interface keep the process engaging and fun
    - There is a wide range for departure dates that allows users to book up to two years in advance
    - Additional departure date flexibility for the Ryanair API can be factored into finding the cheapest flight
    - A wide range of cities and the ranked suitability of each for all occasion and interest parameters offer the user exposure to many different city suggestions
    - The user is given the opportunity to draw and re-draw sets of destination cities as many times as they wish
    - Flight information is offered for each of the three selected cities so that the user can choose a city with booking details in mind
    - A url is provided if desired so that the user can book their flight directly with Ryanair
    - User errors are handled at each stage of input with clear feedback so that the user can find cities and coinciding flights without issue
</details>

# User Experience

## Program Structure

**Instatrip** is a terminal-based application housed on a landing page and deployed by Heroku. It is driven by two core processes, each powered by an API. The first is a data collection and comparison process which measures user input against a Google Sheet of city rankings to determine the user's ideal European destination. The second is a flight retrieval process by which the Ryanair API selects the cheapest flight for the cities decided by the parameters above.

More about each of these processes can be found in the [Flowchart](<#flowchart>) and [Database Structure]((<#database-structure>)) sections. The underlying logic and the user experience navigating through the program can be found in the [Logic Flow](<#logic-flow>) and [Features](<#features>) sections.

## Flowchart  
<details>
<summary> Instatrip Flowchart (click) </summary>
<p align="center">
  <img src="assets/documentation/flowchart.png" height="650px"/>
  </p>

The flow chart for this application was originally designed with pen and paper before I began coding. I used Visio once I had an idea of the general structure and put the first few functions in place. This helped me flesh out the details, stay organized, and create the necessary bridges between functions as the logic of the program grew in complexity
</details>

## Database Structure 

### Google Sheet
<details>
<summary> Instatrip Google Sheet (click) </summary>
<p align="center">
  <img src="assets/documentation/googlesheet.png" height="500px"/>
  </p>

My introduction to Google Sheets was from Code Institute's extremely helpful *Love Sandwiches* walkthrough project. I have often said to my Business Analyst husband that I am not a "spreadsheet person." I was more than pleasantly surprised by the ease of use incorporating these Sheets into both the walkthrough and my own project, and can now officially designate myself a Sheet Believer :sparkles:

My Workbook *Instatrip* consists of a single Sheet. This Sheet is composed of 17 columns, 15 of which form the parameters for the user's travel preferences; and 32 rows, with each row representing a European city.

The column titles are as follows: City, IATA (airport code), Nightlife, History & Culure, Cuisine, Outdoorsy Experiences, Shopping, Off the Beaten Path Exploration, Romantic Adventure, Solo Travel, Hen or Stag Party, Time with Friends or Family, Overall Safety, Accessibility, Public Transportation, Tourism-Friendliness, and English-Speaking

Data to rank each city with a numeric value (1-5) and populate each of the column parameters was collected first from google, and then with the aid of ChatGPT. The program compares these rankings with the user's own ranked preferences to determine which cities make the most suitable destinations 
</details>

### Ryanair API

<details>
<summary>Ryanair API (click)</summary>

I was able to integrate the Ryanair API into this program by signing up for [Rapid API](https://rapidapi.com/DataCrawler/api/ryanair2) and subscribing through their service. This was my second experience with APIs (the first being a soft launch into them with Google Sheets in the *Love Sandwiches* walkthrough), and while the parameters and logic appeared straightforward, I spent an entire morning trying to set it up using SON format before finally turning to AI. One struggle was in fetching the destination airport IATAs, which I eventually stored in my Google Sheet rather than in a list in *run.py*. 

Once integrated, the API made the program functional (a thrill! :woman_dancing:) and I was able to generate flight information through **InstaTrip** and then find the corresponding flights on Ryanair.com
</details>

## Logic Flow

<details>
<summary>Logic Flow (click)</summary>

- The *run.py* file contains all functions for this program. When the site is loaded or the *Run Program* button at the top of the page is clicked, the function *main*() is called.

- *main()* clears the screen of the startup command and prints the **InstaTrip** logo, displays the *Main Menu*, and requests the user to choose a menu option: *Start*, *About*, or *Exit*. The following functions are called for this opening sequence: *colored_instatrip()*, *print_colored_background()*, and *display_menu()*

- When the user chooses the *Start* option, *display_menu()* prints the greeting message (*greeting()*), which gives the user instructions on how to use the program. *Main()* then calls the *get_trip_details()* function, which asks the user for their departure date, departure flexibility, and trip duration. This information will eventually be passed to the Ryanair API.

- Once *get_trip_details()* has run, the user will then be prompted to select their type of trip and choose their important travel factors by functions *type_of_trip()* and *important_factors()*

- This input will then be compared with the data in the *Instatrip* Google Sheet by function *rank_cities()* to order the cities most appropriate to the user's preferences. Function *select_random_cities()* randomizes the order of the cities to avoid listing the first three applicable cities in alphabetical order.

- A *drumroll()* prints and the initial top city selections are displayed. The user is given the choice either to proceed, *generate_new_cities(),* or *start_over()*.

- Function *user_choice_after_ranking()* permits the user to generate three new cities as many times as they wish. The opportunity to proceed, start over, or return to the previous city selections, as stored in the *city_history* list, is given each time. 

- Once the user has selected their preferred three destinations, they are asked by the *rate_importance()* function to rate the importance of five different safety and accessibility factors. Their answers are then compared with the rankings stored in the Sheet for each city, and *adjust_city_scores()* reorders the final three cities from most suitable to least.

- From here, the user's departure data and the IATA airport codes (stored in the Sheet) for the user's selected cities are passed to the Ryanair API. This is accomplished with these functions: *get_airport_codes(), search_ryanair_flights(),* and *find_cheapest_flights()*. The cheapest applicable flight information for each city is then printed and the user may choose whether to *ask_for_booking()* (a url) or *exit()* the program. 

- *Exit()* prints the exit message and art, a url for a staycation article, and the option to return to the *Main Menu*. 
</details>

## Design Choices

### Color Scheme

The color and design scheme for the starting screen of **Instatrip** was chosen to give a slightly nostalgic, retro feel, reminiscent of the travel agency advertisements and city destination posters of yesteryear. The background image for the page, an island sunset, inspired the color choice for the rest of the program. 

While this project by nature limits styling liberties, I enjoyed colorizing the text and making generous use of emoji to compliment the fun, light-hearted tone set by the copy. Booking flights and tending to travel details can often be a dreary affair. The aim here is to break the tedium and usher in a bit of excitement

<p align="center">
    <img src="assets/documentation/bg.png" height="150" style="margin-right: 20px;"/>
    <img src="assets/documentation/logoinspo.png" height="150" style="margin-right: 20px;"/>
    <img src="assets/documentation/emoji.png" height="150" style="margin-right: 20px;"/>
    <img src="assets/documentation/colorama.png" height="150"/>
</p>

- Color for the text was provided by the [Colorama library](https://pypi.org/project/colorama/). The primary colors of choice were Cyan and Magenta, to compliment the background image around the mock terminal. Red was used for exception messages. Red and two tones of Yellow colorized the *Start* screen

- Emoji were taken from the [Emoji for Python library](https://pypi.org/project/emoji/). When using human emoji characters, I made every effort to choose different skintones and genders for inclusivity

### ASCII ART (spelling?)

- ASCII Art for the logo and exit screen has been provided by the [ASCII Art Archive](https://www.asciiart.eu/)  
    
  <p align="center">
  <img src="assets/documentation/startart.png" height="150px"/>
  <img src="assets/documentation/exitart.png" height="150px"/>
  </p>

# Features

I have aimed to give this site a simple, intuitive interface. Ease of navigation allows the visitor to 

Examples of this site's interactive features include:
 
- Example 1
- Example 2

## Favicon

<p align="center">
  <img src="assets/documentation/favicon.png">
</p>

- The favicon features 

## Feature 1

<p align="center">
<img src="assets/documentation/rmstartingarea.png" height="450px"/>
</p>

- Explanation

### Feature 1 sub-feature

<p align="center">
<img src="assets/documentation/rmheading.png" width="250px"/>
</p>

- Explanation

## Feature 2

<p align="center">
<img src="assets/documentation/drawinstructions.png" height="450px"/>
</p>

### Sub-Feature

<p align="center">
<img src="assets/documentation/drawinstructionsh3.png" width="250px"/>
</p>

- Explanation

# Future Features

- A login system to store the user's previously generated cities
- A trip log and diary to record previous travel experiences
- Flexible departure locations rather than the default setting of Dublin airport
- An explanded list of European destinations
- A broader list of trip occasions to select from
- A broader list of preferred activities and interests to select from
- Opening the program to destinations outside of Europe
- Partnerships or tie ins with hotel and car rental accomodations
- Curated experience and activity suggestions
- Flight selection from multiple airlines rather than solely Ryanair
- A proper, clickable link to make a flight booking (currently prevented by Heroku)

# Technologies

## Languages Used

- [Python](https://www.python.org/) - Provides application functionality
- [html](https://developer.mozilla.org/en-US/docs/Web/HTML) - Provides the template for the mock terminal
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Styles the template, including chosen background image

## Libraries, Programs, and Tools

### Python Modules

#### Library Imports:

- [datetime](https://docs.python.org/3/library/datetime.html) - Handles date-based calculations for user travel date
- [os](https://docs.python.org/3/library/os.html) - Clears the terminal
- [random](https://docs.python.org/3/library/random.html#module-random) - Selects elligible cities randomly rather than sequentially
- [textwrap](https://docs.python.org/3/library/textwrap.html#module-textwrap) - Formats text for About section to avoid broken lines
- [time](https://docs.python.org/3/library/time.html#module-time) - Creates "Sleep" pauses to break up lines of text for readability and flare
- [timedelta](https://docs.python.org/3/library/datetime.html#datetime.timedelta) - Class of datetime. Sets date range for departure date

#### Third-Party Imports: 

- [colorama](https://pypi.org/project/colorama/) - Adds color and styles to the project text
- [emoji](https://pypi.org/project/emoji/) - Adds emoji icons to the project
- [gspread](https://pypi.org/project/gspread/) - Stores and Retrieves data from Google Sheets
- [HTTPAdapter](https://pypi.org/project/http-adapter/) - manages HTTP connections with the Ryanair API
- [requests](https://pypi.org/project/requests/) - sends HTTP requests to the Ryanair API
- [Retry](https://pypi.org/project/retry2/) - configures automatic retries for failed network requests to the Ryanair API
- [Ryanair API](https://pypi.org/project/ryanair/) - provides flight information and booking links

#### Other Tools:

- [ASCII Art Archive](https://www.asciiart.eu/) - provides logo and exit screen ASCII art
- [ChatGPT](https://openai.com/chatgpt/) - Assisted in ranking tourist destinations by chosen criteria for Google Sheet
- [Freepik](https://www.freepik.com) - Supplies the landing page background image
- [Github](https://github.com/) - Hosts the code for the site
- [Gitpod](https://www.gitpod.io/#get-started) - Provides the workspace to create and edit the site
- [Google Sheets](https://workspace.google.com/products/sheets/) - Hosts the city data for the application
- [Heroku](https://www.heroku.com) - Deploys the application
- [Icons8](https://icons8.com/) - Supplies the favicon
- [Mistral AI](https://mistral.ai) - For troubleshooting Ryanair API implementation
- [Rapid Api](https://rapidapi.com/) - Integrates the Ryanair API for flight information
- [Visio]( https://www.microsoft.com/en-us/microsoft-365/visio/visio-in-microsoft-365) - Creates the README flowchart

# Testing

## Code Validation

| W3 Validator | views.html | 
|--------------|------------|
| html         | Pass       |


| Python De-linter | run.py | 
|--------------|------------|
| python         | Pass       |


I ran the views.html page housing the terminal through the W3 validator after changing the background. Thankfully, this adjustment caused no errors and the page passed validation.

The Python de-linter----


## Feature Testing 

### Feature Testing Table

<details>

 <summary>A Table of Feature Tests (click)</summary>

| Feature                     | Test Case                 | Outcome                   |
|-----------------------------|---------------------------|---------------------------|
| Favicon | Load Site | Icon and title appear in tab |
| **Section 1**  |
| Feature | Test | Outcome |
| Feature | Test | Outcome |
| **Section 2**  |
| Feature | Test | Outcome |
| Feature | Test | Outcome |
</details>

### Feature Testing Images

<details>
  <summary>Testing the --(click)</summary> 
<p align="center">
<img src="assets/documentation/" height="450px">
</p>

- Feature action 1
- Feature action 2

<p align="center">
<img src="assets/documentation/" height="450px">
</p>

- Feature action 1
- Feature action 2

<p align="center">
<img src="assets/documentation/" height="450px">
</p>
</details>

### HTML Validation
- [W3C HTML Validator](https://validator.w3.org/) -
<details>
    <summary>HTML Validation Screenshot (click)</summary>
     <img src="assets/documentation/">
     <p>No errors were returned</p>
  </details>

### Python Validation
- [Python -- Validator](https://) -
<details>
    <summary>Python Validation Screenshot (click)</summary>
     <img src="assets/documentation/">
     <img src="assets/documentation/">
     <p>No errors returned. etc</p>
  </details>

## Additional Testing

### Lighthouse

<details>
  <summary>Lighthouse Test Results: Mobile (click)</summary> 
<img src="assets/documentation/">
</details>

<details>
  <summary>Lighthouse Test Results: Desktop (click)</summary> 
<img src="assets/documentation/">
</details>

### WAVE Testing

<details>
  <summary>WAVE Web Accessibility Evaluation Tool (click)</summary> 
<img src="assets/documentation/">
<p>Explanation</p>
</details>

### Accessibility
This website was developed with special consideration for accessibility through the following methods:
- Accessibility methods
- Accessibility methods 2

### Manual Testing

if applicable

<details>
  <summary>Screenshots of each area of the site as tested on Am I Responsive? (click)</summary>
   <p align="center">
   <img src="assets/documentation/" width="500px">
   <img src="assets/documentation/" width="500px">
   <img src="assets/documentation/" width="500px">
   <img src="assets/documentation/" width="500px">
   <img src="assets/documentation/" width="500px">
   <img src="assets/documentation/" width="500px">
   </p>
</details>
<details>
  <summary>Screenshots of each area of the site as tested on my own device, iPhone 13Pro (click)</summary>
   <p align="center">
   <img src="assets/documentation/iphone13a.png" height="450px">
   <img src="assets/documentation/iphone13b.png" height="450px">
   <img src="assets/documentation/iphone13c.png" height="450px">
   <img src="assets/documentation/iphone13d.png" height="450px">
   <img src="assets/documentation/iphone13e.png" height="450px">
   <img src="assets/documentation/iphone13f.png" height="450px">
   </p>
</details>

<details>
  <summary>Screenshots of each area of the site as tested on iPhone 11 (click)</summary>
  <p align="center">
   <img src="assets/documentation/iphone11a.PNG" height="450px">
   <img src="assets/documentation/iphone11b.PNG" height="450px">
   <img src="assets/documentation/iphone11c.PNG" height="450px">
   <img src="assets/documentation/iphone11d.PNG" height="450px">
   <img src="assets/documentation/iphone11e.PNG" height="450px">
   <img src="assets/documentation/iphone11f.PNG" height="450px">
   </p>
</details>

<details>
  <summary>Screenshots of each area of the site as tested on HP Elitebook (click)</summary>
   <p align="center">
   <img src="assets/documentation/laptop1a.png" width="500px">
   <img src="assets/documentation/laptop1b.png" width="500px">
   <img src="assets/documentation/laptop1c.png" width="500px">
   <img src="assets/documentation/laptop1d.png" width="500px">
   <img src="assets/documentation/laptop1e.png" width="500px">
   <img src="assets/documentation/laptop1f.png" width="500px">
  </p>
   
</details>

<details>
  <summary>Screenshots of each area of the site as tested on Dell Latitude 5430 (1920px x 1080px) (click)</summary>
  <p align="center">
   <img src="assets/documentation/laptop2a.png" width="500px">
   <img src="assets/documentation/laptop2b.png" width="500px">
   <img src="assets/documentation/laptop2c.png" width="500px">
   <img src="assets/documentation/laptop2d.png" width="500px">
   <img src="assets/documentation/laptop2e.png" width="500px">
   <img src="assets/documentation/laptop2f.png" width="500px">
  </p>
</details>

# Bugs

## Solved Bugs

<details>
  <summary>Bug title (click)</summary>
<img src="assets/documentation/bug1.png">
<p>Explanation and resolution</p>
</details>

## Unsolved Bugs

After implementing the above solutions and running all code through the necessary validators, I am pleased to report no remaining bugs

## Further Areas of Note

I have read that the Code Institute mock terminal does not function properly in Safari. I have been unable to test this myself on a laptop or desktop as I own Windows devices. I can attest that the program does not perform properly on mobile Safari on iPhone, but that is also the case with mobile Chrome. I was not able to implement a solution for this issue as it appears to stem from the terminal and not this program

# Deployment

## To Deploy The Project on Heroku

<details>
  <summary>How to Deploy with Heroku(click)</summary> 
<p>

This site was deployed through Heroku [/?](https://)

1. Instructions 1

![Heroku Deploy Page 1](assets/documentation/deploy1.png)

2. Instructions 2

![Heroku Deploy Page 2](assets/documentation/deploy2.png)

</p>
</details>

## To Fork The Repository on GitHub

<details>
  <summary>How to fork the **InstaTrip** repository (click)</summary>
<p>

To make a copy of a repository, fork it through Github:

1. Find the repository either by using the search bar or by navigating to the URL [/erinvdoyle/instatrip](https://github.com/erinvdoyle/instatrip)
2. Once on the repository main page, navigate to the "Fork" button in the upper-right corner, between the "Watch"("Unwatch" in the image as I am the repository owner and watcher) and "Star" buttons

![Github Fork](assets/documentation/fork.png)

3. Click the "Fork" button to create a copy of the repository. This copy be altered without affecting the source code
</p>
</details>

## Creating A Local Clone of The Project

<details>
  <summary>How to create a local clone (click)</summary>

<p>
To clone the repository of this site:

1. Click the "Code" button in your forked repository

![Github Clone Page 1](assets/documentation/clone1.png)

2. Copy the repository URL (HTTPS, SSH, or GitHub CLI)
3. Open a terminal (or command prompt) on your computer

 ![Github Clone Page 2](assets/documentation/clone2.png)

4. Type the following command: git clone https://github.com/erinvdoyle/instatrip.git to create a local clone

![Github Clone Page 2](assets/documentation/clone3.png)
</p>
</details>


# Credits

## Content

- Code Institute's [Love Sandwiches](https://github.com/erinvdoyle/love_sandwiches) walkthrough project was used as a reference to connect **InstaTrip** to Google Sheets
- The [Code Institute Template](https://github.com/Code-Institute-Org/p3-template) provided everything needed for the mock terminal in the browser

## Technical Content

All tutorials used have been credited throughout the code. Tutorials were consulted as a jumping off point and code was manipulated to perform per my own design and specification

### Python Tutorials

- ["Clear the terminal in Python" Tutorial](https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python)
- ["Exception & Error Handling in Python" Tutorial](https://www.datacamp.com/tutorial/exception-handling-python)
- ["How Do I Create a Scoring System in Python" - Stack Overflow](https://stackoverflow.com/questions/50115873/how-do-i-create-a-scoring-system-in-python)
- ["How to Handle a Python Exception within a Loop" Tutorial](https://www.tutorialspoint.com/how-to-handle-a-python-exception-within-a-loop)
- ["Python Datetime" Tutorial](https://www.w3schools.com/python/python_datetime.asp)
- ["Python Random Module" Tutorial](https://www.w3schools.com/python/module_random.asp)
- ["Sort Using Lambda in Python"](https://sparkbyexamples.com/python/sort-using-lambda-in-python/) 


## Media
### Image Credits

- [Main Image by FreePik](https://www.freepik.com/free-vector/gradient-beach-sunset-landscape_4636385.htm)
- [Retro Logo Inspiration by Sundhar on Dribble](https://dribbble.com/shots/7900685-Retro-Logo-Design)

# Acknowledgements

- My mentor, Precious Ijege, for helping me make sure all my exceptions were handled, providing kind guidance from project inception to completion, and allowing me to see the project with fresh eyes.
- Our cohort standup leader, Kay Welfare, for providing a weekly dose of enthusiasm and encouragement
- The CI Hackathon staff and my Elevate Hackathon teammates (Team ResuMates!) for inspiration and the opportunity to experience working as part of a team
- My husband, Taylor, process mapper extraordinaire, for helping me tighten up my flow chart. And *especially* for taking care of our horses and household during Storm Ashley to allow me long hours to complete the bulk of this project

# Contact

Thank you for viewing this project. Please feel free to contact me with any questions, comments, or opportunities
  
 - [erin.v.doyle@gmail.com](mailto:erin.v.doyle@gmail.com)
 - [linkedin.com/erinvdoyle](https://linkedin.com/erinvdoyle)
