import streamlit as st
import pandas as pd
import numpy as np
import base64
import io
import datetime

def app():
    st.title("화천 ScoreCard")

    # 현재 날짜 가져오기
    current_date = datetime.date.today()

    # Streamlit 앱에 현재 날짜 출력, 년-월-일 형식으로
    st.subheader(current_date.strftime('%Y년 %m월 %d일'))

    # 홀 이름과 거리 설정
    holes = ['A1_Par4(92m)', 'A2_Par3(58m)', 'A3_Par3(50m)', 'A4_Par4(80m)', 
            'A5_Par4(100m)', 'A6_Par3(60m)', 'A7_Par3(60m)', 'A8_Par5(130m)', 'A9_Par4(70m)', 
            'B1_Par4(85m)', 'B2_Par3(50m)', 'B3_Par4(90m)', 'B4_Par3(55m)', 
            'B5_Par3(58m)', 'B6_Par4(85m)', 'B7_Par3(55m)', 'B8_Par4(88m)', 'B9_Par5(150m)',
            'C1_Par3(50m)', 'C2_Par5(110m)', 'C3_Par3(45m)', 'C4_Par4(80m)', 
            'C5_Par4(75m)', 'C6_Par4(90m)', 'C7_Par4(88m)', 'C8_Par3(50m)', 'C9_Par3(50m)',
            'D1_Par3(46m)', 'D2_Par3(41m)', 'D3_Par4(65m)', 'D4_Par3(52m)', 
            'D5_Par4(75m)', 'D6_Par3(50m)', 'D7_Par4(70m)', 'D8_Par4(85m)', 'D9_Par5(135m)']

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

     # st.download_button을 이용해 excel 파일을 다운로드 링크로 제공합니다.
        st.download_button(label='점수카드 다운로드',
                            data=excel_data,
                            file_name='scorecard.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        if st.button("점수카드 저장"):
            with open('scorecard.xlsx', 'wb') as f:
                f.write(excel_data)


if __name__ == "__main__":
    app()
