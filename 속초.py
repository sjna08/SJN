import streamlit as st
import pandas as pd
import sqlite3
import base64
import io
import datetime

def app():
    conn = sqlite3.connect(':memory:', check_same_thread=False)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS scorecard (
            player TEXT,
            hole TEXT,
            score INTEGER,
            PRIMARY KEY (player, hole)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS players (
            name TEXT
        )
    """)

    conn.execute("DELETE FROM players")
    conn.commit()

    st.title("속초 ScoreCard")

    current_date = datetime.date.today()

    st.subheader(current_date.strftime('%Y년 %m월 %d일'))

 
      # 홀 이름과 거리 설정
    holes = ['A1_Par3(58m)', 'A2_Par4(65m)', 'A3_Par3(53m)', 'A4_Par4(72m)', 
            'A5_Par4(90m)', 'A6_Par5(120m)', 'A7_Par3(45m)', 'A8_Par3(50m)', 'A9_Par4(96m)', 
            'B1_Par4(72m)', 'B2_Par4(68m)', 'B3_Par5(120m)', 'B4_Par3(60m)', 
            'B5_Par3(58m)', 'B6_Par3(58m)', 'B7_Par4(70m)', 'B8_Par4(70m)', 'B9_Par3(50m)',
            'C1_Par3(58m)', 'C2_Par4(65m)', 'C3_Par3(53m)', 'C4_Par4(72m)', 
            'C5_Par4(90m)', 'C6_Par5(120m)', 'C7_Par3(45m)', 'C8_Par3(50m)', 'C9_Par4(96m)', 
            'D1_Par4(72m)', 'D2_Par4(68m)', 'D3_Par5(120m)', 'D4_Par3(60m)', 
            'D5_Par3(58m)', 'D6_Par3(58m)', 'D7_Par4(70m)', 'D8_Par4(70m)', 'D9_Par3(50m)']

    
    num_players = 4
    players = [st.sidebar.text_input(f'Player {i+1} 이름', value=f'Player{i+1}') for i in range(num_players)]
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

    for hole in selected_holes:
        hole_name = f'<h3><strong>{hole}</strong></h3>'
        st.markdown(hole_name, unsafe_allow_html=True)

        for player in players:
            score = conn.execute("SELECT score FROM scorecard WHERE player=? AND hole=?", (player, hole)).fetchone()
            score = score[0] if score else 0
            score = st.number_input(f'{player} {hole} 점수', min_value=0, value=int(score), key=f'{player}_{hole}', format="%d")
            
            conn.execute("""
                INSERT OR REPLACE INTO scorecard (player, hole, score)
                VALUES (?, ?, ?)
            """, (player, hole, score))
            conn.commit()

    if st.button('제출'):
        df = pd.read_sql_query("SELECT * from scorecard", conn)
        df = df.pivot(index='player', columns='hole', values='score')

        summary = pd.DataFrame(index=players, columns=['TTL','A','B','C','D', 'A_Dif','B_Dif','C_Dif','D_Dif','TTL_Dif'])
        summary['A'] = df.iloc[:, :9].sum(axis=1)
        summary['B'] = df.iloc[:, 9:18].sum(axis=1)
        summary['C'] = df.iloc[:, 18:27].sum(axis=1)
        summary['D'] = df.iloc[:, 27:].sum(axis=1)
        summary['TTL'] = summary['A'] + summary['B'] + summary['C'] + summary['D']

        summary['A_Dif'] = summary['A'] - 33
        summary['B_Dif'] = summary['B'] - 33
        summary['C_Dif'] = summary['C'] - 33
        summary['D_Dif'] = summary['D'] - 33
        summary['TTL_Dif'] = summary['TTL'] - 132

        full_df = pd.concat([summary, df], axis=1).fillna(0).astype(int)

        st.write(full_df)

        excel_buffer = io.BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            full_df.to_excel(writer, index=True)

        excel_data = excel_buffer.getvalue()

        st.download_button(label='점수카드 다운로드',
                        data=excel_data,
                        file_name=f'점수카드_{current_date.strftime("%Y%m%d")}.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
        conn.execute("DELETE FROM scorecard")
        conn.commit()

    conn.close()

if __name__ == "__main__":
    app()
