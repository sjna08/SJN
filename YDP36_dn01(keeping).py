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

    # Database setup
    conn = sqlite3.connect(':memory:')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS scorecard (
        player TEXT,
        hole TEXT,
        score INTEGER,
        PRIMARY KEY(player, hole)
    )
    ''')

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

    # Save player names to database
    conn.execute("DELETE FROM players")
    for player in players:
        conn.execute("INSERT INTO players (name) VALUES (?)", (player,))
    conn.commit()

    page = st.sidebar.radio('페이지 선택', ['A&B 홀', 'C&D 홀', '전체'])

    if page == 'A&B 홀':
        selected_holes = holes[:18]
    elif page == 'C&D 홀':
        selected_holes = holes[18:]
    else:
        selected_holes = holes

   # 스코어카드 생성
    scorecard = pd.DataFrame(index=players, columns=holes)

    # Display scorecard for input
    for hole in selected_holes:
       hole_name = f'<h3><strong>{hole}</strong></h3>'
       st.markdown(hole_name, unsafe_allow_html=True)
        
       for player in players:
            # Retrieve score from database
            cursor = conn.execute("SELECT score FROM scorecard WHERE player=? AND hole=?", (player, hole))
            row = cursor.fetchone()
            default_value = row[0] if row else 0

            score = st.number_input(f'{player} {hole} 점수', min_value=0, value=int(default_value), key=f'{player}_{hole}', format="%d")

            # Update score in database
            conn.execute("INSERT OR REPLACE INTO scorecard (player, hole, score) VALUES (?, ?, ?)", (player, hole, score))
            conn.commit()

    # If the reset button is pressed, delete all scores from the database
    if st.button('점수 초기화'):
        conn.execute("DELETE FROM scorecard")
        conn.commit()

    # Submit scores and calculate summary
    if st.button('제출'):
        # Load scorecard from database
        cursor = conn.execute("SELECT player, hole, score FROM scorecard")
        rows = cursor.fetchall()
        scorecard = pd.DataFrame(rows, columns=["Player", "Hole", "Score"]).pivot("Player", "Hole", "Score")
        scorecard.fillna(0, inplace=True)

        summary = pd.DataFrame(index=players, columns=['TTL','A','B', 'A_Dif','B_Dif','C','D', 'C_Dif','D_Dif','TTL_Dif'])
        summary['A'] = scorecard.iloc[:, :9].sum(axis=1)
        summary['B'] = scorecard.iloc[:, 9:18].sum(axis=1)
        summary['C'] = scorecard.iloc[:, 18:27].sum(axis=1)
        summary['D'] = scorecard.iloc[:, 27:].sum(axis=1)
        summary['TTL'] = summary['A'] + summary['B'] + summary['C'] + summary['D']

        summary['A_Dif'] = summary['A'] - 33
        summary['B_Dif'] = summary['B'] - 33
        summary['C_Dif'] = summary['C'] - 33
        summary['D_Dif'] = summary['D'] - 33
        summary['TTL_Dif'] = summary['TTL'] - 132

        st.write(summary.fillna(0).astype(int))
        st.write(scorecard.fillna(0).astype(int))

        full_scorecard = pd.concat([summary, scorecard], axis=1)

         # Excel 파일을 메모리에 저장하기 위한 버퍼를 생성합니다.
        excel_buffer = io.BytesIO()

        # 판다스의 ExcelWriter를 사용하여 메모리에 엑셀 파일을 작성합니다.
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            full_scorecard.to_excel(writer, sheet_name='Sheet1')

        # 스트림리트로 작성된 엑셀 파일을 다운로드 링크로 제공합니다.
        excel_buffer.seek(0)
        b64 = base64.b64encode(excel_buffer.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="scorecard_{current_date}.xlsx">점수카드 다운로드(엑셀파일)</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Reset scorecard after submission
        conn.execute("DELETE FROM scorecard")
        conn.commit()

if __name__ == "__main__":
    app()
