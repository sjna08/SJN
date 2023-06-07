def app():
    import streamlit as st
    import pandas as pd
    import base64
    import io
    import os

    st.title("ParkGolf ScoreCard")

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
    players = [st.sidebar.text_input(f'Player {i+1}이름',value=f'Player{i+1}') for i in range(num_players)]

    page = st.sidebar.radio('페이지 선택', ['A&B 홀', 'C&D 홀', '전체'])

    if page == 'A&B 홀':
        selected_holes = holes[:18]
    elif page == 'C&D 홀':
        selected_holes = holes[18:]
    else:
        selected_holes = holes

    if 'scorecard' not in st.session_state:
        st.session_state['scorecard'] = pd.DataFrame(index=players, columns=holes)
    scorecard = st.session_state['scorecard']

    for hole in selected_holes:
        st.subheader(hole)
        for player in players:
            scorecard.loc[player, hole] = st.number_input(f'{player} {hole} 점수', min_value=0, value=0, key=f'{player}_{hole}')
    
    # 데이터를 저장하거나 로드하는 기능
    if st.button('저장'):
        st.session_state['scorecard'].to_csv('scorecard.csv', encoding='utf-8-sig')
        st.success("저장되었습니다.")
    if st.button('로드'):
        if os.path.exists('scorecard.csv'):
            st.session_state['scorecard'] = pd.read

if __name__ == "__main__":
   app()
