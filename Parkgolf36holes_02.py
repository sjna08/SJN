import streamlit as st
import pandas as pd
import base64
import io

# Main Page
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

# 플레이어 수 설정
num_players = 4
players = [st.sidebar.text_input(f'Player {i+1}이름',value=f'Player{i+1}') for i in range(num_players)]

# 페이지 설정
page = st.sidebar.radio('페이지 선택', ['A&B 홀', 'C&D 홀', '전체'])

if page == 'A&B 홀':
    selected_holes = holes[:18]
elif page == 'C&D 홀':
    selected_holes = holes[18:]
else:
    selected_holes = holes

# 스코어카드 생성
if 'scorecard' not in st.session_state:
    st.session_state['scorecard'] = pd.DataFrame(index=players, columns=holes)
scorecard = st.session_state['scorecard']

# 사용자에게 입력 받기
for hole in selected_holes:
    st.subheader(hole)
    for player in players:
        scorecard.loc[player, hole] = st.number_input(f'{player} {hole} 점수', min_value=0, value=0, key=f'{player}_{hole}')

# 입력 받은 정보를 표시하고 다운로드 받기
if st.button('제출'):
    summary = pd.DataFrame(index=players, columns=['TTL','A','B', 'A_Dif','B_Dif','C','D', 'C_Dif','D_Dif','TTL_Dif'])
    summary['A'] = scorecard.iloc[:, :9].sum(axis=1)
    summary['B'] = scorecard.iloc[:, 9:18].sum(axis=1)
    summary['C'] = scorecard.iloc[:, 18:27].sum(axis=1)
    summary['D'] = scorecard.iloc[:, 27:].sum(axis=1)
    summary['TTL'] = summary['A
