# Import necessary libraries
import streamlit as st
import pandas as pd
import base64
import io

# Main title
st.title("ParkGolf ScoreCard")

# Hole names and distances
holes = ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 
         'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)', 
         'B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 
         'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)',
         'C1_Par4(60m)', 'C2_Par3(40m)', 'C3_Par3(65m)', 'C4_Par4(100m)', 
         'C5_Par5(130m)', 'C6_Par4(72m)', 'C7_Par4(81m)', 'C8_Par3(50m)', 'C9_Par3(50m)',
         'D1_Par3(69m)', 'D2_Par4(100m)', 'D3_Par4(68m)', 'D4_Par3(50m)', 
         'D5_Par4(58m)', 'D6_Par3(55m)', 'D7_Par4(71m)', 'D8_Par5(123m)', 'D9_Par3(66m)']

# Number of players
num_players = 4
players = [st.sidebar.text_input(f'Player {i+1} name',value=f'Player{i+1}') for i in range(num_players)]

# Page selection
page = st.sidebar.radio('Choose page', ['A&B Holes', 'C&D Holes', 'All'])

if page == 'A&B Holes':
    selected_holes = holes[:18]
elif page == 'C&D Holes':
    selected_holes = holes[18:]
else:
    selected_holes = holes

# Create scorecard
if 'scorecard' not in st.session_state:
    st.session_state['scorecard'] = pd.DataFrame(index=players, columns=holes)
scorecard = st.session_state['scorecard']

# Get input from users
for hole in selected_holes:
    st.subheader(hole)
    for player in players:
        scorecard.loc[player, hole] = st.number_input(f'{player} score for {hole}', min_value=0, value=0, key=f'{player}_{hole}')

# Show input and provide download
if st.button('Submit'):
    summary = pd.DataFrame(index=players, columns=['TTL','A','B', 'A_Dif','B_Dif','C','D', 'C_Dif','D_Dif','TTL_Dif'])
    summary['A'] = scorecard.iloc[:, :9].sum(axis=1)
    summary['B'] = scorecard.iloc[:, 9:

 
