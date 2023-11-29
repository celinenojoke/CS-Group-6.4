import streamlit as st
from google_route_planner import GoogleRouteFinder

def main_page():
    st.title("Welcome to the Route Planner")
    
def route_input_page():
    st.title("Route Planner")
    start_location = st.text_input("Start Location", "Bern, Switzerland")
    end_location = st.text_input("End Location", "Zurich, Switzerland")
    departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM:SS)")
    
    if st.button("Find Route"):
        route_finder = GoogleRouteFinder()
        route_info = route_finder.get_shortest_route(start_location, end_location, departure_time)
        st.write(route_info)
        
    
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page", ["Home", "Route Planner"])

if page == "Home":
    main_page()
elif page == "Route Planner":
    route_input_page()