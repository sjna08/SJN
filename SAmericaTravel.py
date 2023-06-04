import streamlit as st

# Main Page
st.title("South America Trip Planner")

# Flight Information
st.header("Flight Information")

flight_departure = st.text_input("Enter Departure Location for Flight")
flight_destination = st.text_input("Enter Destination for Flight")
flight_date = st.date_input("Enter Date for Flight")

if flight_departure and flight_destination and flight_date:
    # API 호출이나 실제 작업을 여기에 추가합니다.
    st.write(f"Searching for flights from {flight_departure} to {flight_destination} on {flight_date}.")
else:
    st.write("Please enter flight details.")

# Hotel Information
st.header("Hotel Information")

hotel_location = st.text_input("Enter Location for Hotel")
hotel_check_in = st.date_input("Enter Check-in Date for Hotel")
hotel_check_out = st.date_input("Enter Check-out Date for Hotel")

if hotel_location and hotel_check_in and hotel_check_out:
    # API 호출이나 실제 작업을 여기에 추가합니다.
    st.write(f"Searching for hotels in {hotel_location} from {hotel_check_in} to {hotel_check_out}.")
else:
    st.write("Please enter hotel details.")
