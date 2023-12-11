import googlemaps
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class GoogleRouteFinder:
    def __init__(self):
        self.api_key = os.getenv('GMAP_API_KEY')
        self.client=googlemaps.Client(key=self.api_key)

    # arrival time is when the train arrives
    # this method calculates the departure time
    def find_departure_time(self, start, end, arrival_time_str):
        # Parse the departure time string into a datetime object
        try:
            #change arrival time from string to date
            arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return "Invalid departure time format. Please use YYYY-MM-DD HH:MM:SS"

        # Request directions for a certain arrival time
        directions_result = self.client.directions(origin=start, destination=end, arrival_time=arrival_time)

        # Extract the route information
        # check if direction results are empty - if not proceed
        if directions_result:
            route = directions_result[0]['legs'][0]
            print(route)
            # duration of the route in seconds
            duration_seconds = route['duration']['value']
            # arrival time is of format Ymd HMS --> the seconds has to be distracted which should lead to the expected departure time
            # maybe the departure time can be read out of the route, which would make sense
            # this has to be tested
            expected_departure_time = arrival_time - timedelta(seconds=duration_seconds)
            return {
                'start_point': route['start_address'],
                'end_point': route['end_address'],
                'date': arrival_time.strftime("%Y-%m-%d"),
                'expected_departure_time': expected_departure_time.strftime("%H:%M:%S"),
                'distance': route['distance']['text'],
                'duration': route['duration']['text']
            }
        else:
            return "No route found"
        
    def get_shortest_route(self, start, end, departure_time_str):
        # Parse the departure time string into a datetime object
        try:
            departure_time = datetime.strptime(departure_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return "Invalid departure time format. Please use YYYY-MM-DD HH:MM:SS"

        # Request directions
        directions_result = self.client.directions(start, end, departure_time=departure_time)

        # Extract the route information
        if directions_result:
            route = directions_result[0]['legs'][0]
            duration_seconds = route['duration']['value']
            expected_arrival_time = departure_time + timedelta(seconds=duration_seconds)
            return {
                'start_point': route['start_address'],
                'end_point': route['end_address'],
                'date': departure_time.strftime("%Y-%m-%d"),
                'departure_time': departure_time.strftime("%H:%M:%S"),
                'expected_arrival_time': expected_arrival_time.strftime("%H:%M:%S"),
                'distance': route['distance']['text'],
                'duration': route['duration']['text']
            }
        else:
            return "No route found"
    
    def get_via_route(self, start, end, waypoint, departure_time_str):
        # Parse the departure time string into a datetime object
        try:
            departure_time = datetime.strptime(departure_time_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return "Invalid departure time format. Please use YYYY-MM-DD HH:MM:SS"

        # Request directions with waypoint
        directions_result = self.client.directions(start, end, waypoints=[waypoint], departure_time=departure_time)

        # Extract the route information
        if directions_result:
            total_distance = 0
            total_duration = timedelta()
            for leg in directions_result[0]['legs']:
                total_distance += leg['distance']['value']  # Summing up distance of all legs
                total_duration += timedelta(seconds=leg['duration']['value'])  # Summing up duration of all legs
            
            expected_arrival_time = departure_time + total_duration

            return {
                'start_point': start,
                'waypoint': waypoint,
                'end_point': end,
                'date': departure_time.strftime("%Y-%m-%d"),
                'departure_time': departure_time.strftime("%H:%M:%S"),
                'expected_arrival_time': expected_arrival_time.strftime("%H:%M:%S"),
                'total_distance': f"{total_distance/1000:.2f} km",  # Convert to km
                'total_duration': str(total_duration)
            }
        else:
            return "No route found"
