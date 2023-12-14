# Import nevessary libraries
import streamlit as st
import googlemaps
import requests
from datetime import datetime, timedelta

# Define a function to get the duration in traffic from Google Maps API
def get_google_maps_duration(api_key, origin, destination, departure_time):
    gmaps = googlemaps.Client(key="Place your Google Maps API Key")
    # Get directions from the origin to the destination using driving mode and departure time
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=departure_time)
    # Extract the duration in traffic from the response
    duration_in_traffic = directions_result[0]['legs'][0]['duration_in_traffic']['value']
    return duration_in_traffic

# Definition of a function to convert duration strings to seconds
def convert_duration_to_seconds(duration_str):
    days, rest = duration_str.split('d')
    hours, minutes, seconds = map(int, rest.split(':'))
    total_seconds = int(days) * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60 + seconds
    return total_seconds

# Definition of a function to get train duration using the Swiss public transportation API
def get_train_duration(start_location_train, selected_destination, departure_time_train):
    url = 'http://transport.opendata.ch/v1/connections'
    params = {
        'from': start_location_train,
        'to': selected_destination,
        'limit': 1,
        'date': departure_time_train.strftime('%Y-%m-%d'),
        'time': departure_time_train.strftime('%H:%M:%S'),
    }
    # Rquest to Swiss public transportation API
    response = requests.get(url, params=params)
    # parse JSON response
    data = response.json()
    # Extract the duration from the connections Data
    connections = data.get('connections', [])
    if connections:
        duration = connections[0].get('duration', '0d00:00:00')
        return convert_duration_to_seconds(duration)
    else:
        # Case where no connections are found
        return float('inf')

# Definition of a function to convert seconds to hours and minutes
def seconds_to_hours_minutes(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return hours, minutes

# Definition of the main page for user input using Streamlit
def route_input_page():
    # Get user input
    start_location_car = st.text_input("Start Location Car", "St. Gallen, Switzerland")
    start_location_train = st.text_input("Start Location Train", "Basel, Switzerland")
    departure_time_train_input = st.text_input("Departure Time Train (YYYY-MM-DD HH:MM:SS)")

    # Button to start the calculation
    if st.button("Calculate"):
        # Validation and parse the train departure time input
        if departure_time_train_input:
            try:
                departure_time_train = datetime.strptime(departure_time_train_input, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                st.error("Invalid date/time format. Please enter the correct format (YYYY-MM-DD HH:MM:SS).")
                return
        else:
            st.error("Please enter a departure time for the train.")
            return

        # Hardcoded destinations to minimize calculaiton time
        destinations = [
            'Zürich HB, Switzerland', 'Bern, Switzerland', 'Basel, Switzerland',
            'Lausanne, Switzerland', 'Winterthur, Switzerland', 'Zürich Oerlikon, Switzerland',
            'Zürich Stadelhofen, Switzerland', 'Genf, Switzerland', 'Zürich Hardbrücke, Switzerland',
            'St. Gallen, Switzerland', 'Zürich Flughafen, Switzerland', 'Biel, Switzerland',
            'Zug, Switzerland', 'Baden, Switzerland', 'Zürich Altstetten, Switzerland',
            'Thun, Switzerland', 'Neuchâtel, Switzerland', 'Chur, Switzerland', 'Uster, Switzerland',
            'Rapperswil, Switzerland', 'Freiburg, Switzerland', 'Brugg, Switzerland', 'Vevey, Switzerland',
            'Stettbach, Switzerland', 'Dietikon, Switzerland', 'Visp, Switzerland', 'Renens, Switzerland',
            'Thalwil, Switzerland', 'Luzern, Switzerland'
        ]


        # API Key for Google Maps API
        api_key = "Place your Google Maps API Key"

        # Initiation of variables for optimal route information
        min_total_duration = float('inf')
        optimal_destination = None
        optimal_car_duration = None
        optimal_train_duration = None

        # Loop for each destination to find the optimal route
        for selected_destination in destinations:
            # Get car and train durations for the current destination
            car_duration = get_google_maps_duration(api_key, start_location_car, selected_destination, departure_time_train)
            train_duration = get_train_duration(start_location_train, selected_destination, departure_time_train)

            # Calculation of the total duration for the current destination
            total_duration = car_duration + train_duration

            # Update optimal route information if the current route is better
            if total_duration < min_total_duration:
                min_total_duration = total_duration
                optimal_destination = selected_destination
                optimal_car_duration = car_duration
                optimal_train_duration = train_duration

        # Display of the optimal route information 
        if optimal_destination is not None:
            # Convert durations to hours and minutes
            optimal_total_hours, optimal_total_minutes = seconds_to_hours_minutes(min_total_duration)
            optimal_car_hours, optimal_car_minutes = seconds_to_hours_minutes(optimal_car_duration)
            optimal_train_hours, optimal_train_minutes = seconds_to_hours_minutes(optimal_train_duration)

            # Calculation of arrival and departure times
            arrival_time_car = departure_time_train + timedelta(seconds=optimal_car_duration)
            arrival_time_train = departure_time_train + timedelta(seconds=optimal_train_duration)
            arrival_time_car_hours, arrival_time_car_minutes = arrival_time_car.hour, arrival_time_car.minute
            arrival_time_train_hours, arrival_time_train_minutes = arrival_time_train.hour, arrival_time_train.minute

            # Calculation of departure time of the car
            departure_time_car = departure_time_train - timedelta(seconds=optimal_car_duration)
            departure_time_car_hours, departure_time_car_minutes = departure_time_car.hour, departure_time_car.minute

            # Display Streamlit responses separately
            st.write(f"Optimal Destination: {optimal_destination}")
            st.write(f"Total Duration: {optimal_total_hours} hours and {optimal_total_minutes} minutes")

            st.write(f"Departure Time Car: {departure_time_car_hours:02}:{departure_time_car_minutes:02}")
            st.write(f"Arrival Time Car: {arrival_time_car_hours:02}:{arrival_time_car_minutes:02}")
            st.write(f"Car Duration: {optimal_car_hours} hours and {optimal_car_minutes} minutes")

            st.write(f"Departure Time Train: {departure_time_train.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"Arrival Time Train: {arrival_time_train_hours:02}:{arrival_time_train_minutes:02}")
            st.write(f"Train Duration: {optimal_train_hours} hours and {optimal_train_minutes} minutes")

 

# direct execution of the Streamlit App
if __name__ == "__main__":
    route_input_page()