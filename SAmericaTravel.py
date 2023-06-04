import streamlit as st

# Sidebar
st.sidebar.title("API Inputs")
flight = st.sidebar.text_input("Enter Flight Details")
hotel = st.sidebar.text_input("Enter Hotel Details")

# Main Page
st.title("South America Trip Planner")

st.header("Flight Information")
if flight:
    # API 호출이나 실제 작업을 여기에 추가합니다.
    st.write(f"Searching for flight: {flight}")
else:
    st.write("Please enter flight details in the sidebar.")

st.header("Hotel Information")
if hotel:
    # API 호출이나 실제 작업을 여기에 추가합니다.
    st.write(f"Searching for hotel: {hotel}")
else:
    st.write("Please enter hotel details in the sidebar.")
