import googlemaps
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class GoogleRouteFinder:
    def __init__(self):
        self.api_key = os.getenv('GMAP_API_KEY')
        self.client=googlemaps.Client(key=self.api_key)
        
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
    
   