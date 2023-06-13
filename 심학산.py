import streamlit as st
import pandas as pd
import numpy as np
import base64
import io

def app():
    st.title("ParkGolf ScoreCard")

    # 홀 이름과 거리 설정
    holes = ['A1_Par4(62m)', 'A2_Par3(41m)', 'A3_Par4(67m)', 'A4_Par3(40m)', 
            'A5_Par5(100m)', 'A6_Par3(52m)', 'A7_Par4(60m)', 'A8_Par3(40m)', 'A9_Par4(62m)', 
            'B1_Par4(68m)', 'B2_Par4(62m)', 'B3_Par3(41m)', 'B4_Par5(100m)', 
            'B5_Par3(50m)', 'B6_Par3(52m)', 'B7_Par4(72m)', 'B8_Par3(40m)', 'B9_Par4(67m)',
            'C1_Par4(62m)', 'C2_Par3(41m)', 'C3_Par4(67m)', 'C4_Par3(40m)', 
            'C5_Par5(100m)', 'C6_Par3(52m)', 'C7_Par4(60m)', 'C8_Par3(40m)', 'C9_Par4(62m)',
            'D1_Pa4(68m)', 'D2_Par4(62m)', 'D3_Par3(41m)', 'D4_Par5(100m)', 
            'D5_Par3(50m)', 'D6_Par3(52m)', 'D7_Par4(72m)', 'D8_Par3(40m)', 'D9_Par4(67m)']

    num_players = 4
    players = [st.sidebar.text_input(f'Player {i+1} 이름', value=f'Player{i+1}') for i in range(num_players)]

    page = st.sidebar.radio('페이지 선택', ['A&B 홀', 'C&D 홀', '전체'])

    if page == 'A&B 홀':
        selected_holes = holes[:18]
    elif page == 'C&D 홀':
        selected_holes = holes[18:]
    else:
        selected_holes = holes

   # 스코어카드 생성
    scorecard = pd.DataFrame(index=players, columns=holes)

    # Create or load scorecard
    if 'scorecard' not in st.session_state:
        st.session_state['scorecard'] = pd.DataFrame(index=players, columns=holes)
    elif st.button("저장된 점수카드 불러오기"):
        try:
            st.session_state['scorecard'] = pd.read_excel('scorecard.xlsx', index_col=0)
        except FileNotFoundError:
            st.warning("저장된 점수카드를 찾을 수 없습니다.")

    # Update player names
    st.session_state['scorecard'].index = players

    # Display scorecard for input
    scorecard = st.session_state['scorecard']
    for hole in selected_holes:
       hole_name = f'<h3><strong>{hole}</strong></h3>'
       st.markdown(hole_name, unsafe_allow_html=True)
        
       for player in players:
            default_value = scorecard.loc[player, hole] if not pd.isna(scorecard.loc[player, hole]) else 0
            score = st.number_input(f'{player} {hole} 점수', min_value=0, value=int(default_value), key=f'{player}_{hole}', format="%d")
            scorecard.loc[player, hole] = score

    # Update scorecard in session state
    st.session_state['scorecard'] = scorecard

    # Submit scores and calculate summary
    if st.button('제출'):
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
        
        # DataFrame을 Excel 파일로 저장합니다.
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            full_scorecard.to_excel(writer, index=True)

        # 버퍼에 저장된 데이터를 가져옵니다.
        excel_data = excel_buffer.getvalue()

        # Excel 데이터를 base64 형식으로 인코딩합니다.
        b64 = base64.b64encode(excel_data).decode()

        # 다운로드 링크를 만들고 Streamlit 앱에 표시합니다.
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="scorecard.xlsx">Download XLSX File</a>'
        st.markdown(href, unsafe_allow_html=True)

        if st.button("점수카드 저장"):
            with open('scorecard.xlsx', 'wb') as f:
                f.write(excel_data)


if __name__ == "__main__":
    app()
