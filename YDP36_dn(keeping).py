import streamlit as st
import pandas as pd
import numpy as np
import base64
import io
import datetime
import sqlite3

def app():
    st.title("YDP ScoreCard")

    # 현재 날짜 가져오기
    current_date = datetime.date.today()

    # Streamlit 앱에 현재 날짜 출력, 년-월-일 형식으로
    st.subheader(current_date.strftime('%Y년 %m월 %d일'))

    # 홀 이름과 거리 설정
    holes = ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 
            'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)', 
            'B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 
            'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)',
            'C1_Par4(60m)', 'C2_Par3(40m)', 'C3_Par3(65m)', 'C4_Par4(100m)', 
            'C5_Par5(130m)', 'C6_Par4(72m)', 'C7_Par4(81m)', 'C8_Par3(50m)', 'C9_Par3(50m)',
            'D1_Par3(69m)', 'D2_Par4(100m)', 'D3_Par4(68m)', 'D4_Par3(50m)', 
            'D5_Par4(58m)', 'D6_Par3(55m)', 'D7_Par4(71m)', 'D8_Par5(123m)', 'D9_Par3(66m)']

    num_players = 4
    players = [st.sidebar.text_input(f'Player {i+1} 이름', value=f'Player{i+1}') for i in range(num_players)]

    page = st.sidebar.radio('페이지 선택', ['A&B 홀', 'C&D 홀', '전체'])

    if page == 'A&B 홀':
        selected_holes = holes[:18]
    elif page == 'C&D 홀':
        selected_holes = holes[18:]
    else:
        selected_holes = holes

    # Create a new database or open a connection to an existing one
    conn = sqlite3.connect('scorecard.db')

    # Create a new table for the scorecard if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS scorecard (
            player TEXT,
            hole TEXT,
            score INTEGER,
            PRIMARY KEY (player, hole)
        )
    ''')

    # Update player names and load existing scores
    st.session_state['scorecard'] = pd.DataFrame(index=players, columns=holes)
    for player in players:
        for hole in holes:
            # Try to load the score for this player and hole from the database
            score = conn.execute('SELECT score FROM scorecard WHERE player = ? AND hole = ?', (player, hole)).fetchone()
            if score is not None:
                st.session_state['scorecard'].loc[player, hole] = score[0]

    # Display scorecard for input
    scorecard = st.session_state['scorecard']
    for hole in selected_holes:
        hole_name = f'<h3><strong>{hole}</strong></h3>'
        st.markdown(hole_name, unsafe_allow_html=True)

        for player in players:
            default_value = scorecard.loc[player, hole] if not pd.isna(scorecard.loc[player, hole]) else 0
            score = st.number_input(f'{player} {hole} 점수', min_value=0, value=int(default_value), key=f'{player}_{hole}', format="%d")
            scorecard.loc[player, hole] = score

            # Update the score for this player and hole in the database
            conn.execute('REPLACE INTO scorecard (player, hole, score) VALUES (?, ?, ?)', (player, hole, score))

    # Update scorecard in session state
    st.session_state['scorecard'] = scorecard

    # Submit scores and calculate summary
    if st.button('제출'):
        # ... (나머지 코드는 원래와 동일하게 유지)

    # Save changes to the database and close the connection when the app is done
    conn.commit()
    conn.close()


if __name__ == "__main__":
    app()
