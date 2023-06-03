# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd

# Streamlit 앱 시작
def app():
    # 플레이어 수 설정
    num_players = 4
    players = [st.sidebar.text_input(f'Player {i+1} 이름', value=f'Player {i+1}') for i in range(num_players)]

    # 홀 이름과 거리 설정
    holes = ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 
             'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)', 
             'B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 
             'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)']

    # 스코어카드 생성
    scorecard = pd.DataFrame(index=players, columns=holes)

    # 사용자에게 입력 받기
    for hole in holes:
        st.subheader(hole)
        for player in players:
            scorecard.loc[player, hole] = st.number_input(f'{player} {hole} 점수', min_value=0, value=0, key=f'{player}_{hole}')

    # 입력 받은 정보를 표시하기
    if st.button('제출'):
        summary = pd.DataFrame(index=players, columns=['총점', 'A홀점수', 'B홀점수'])
        summary['A홀점수'] = scorecard.iloc[:, :9].sum(axis=1)
        summary['B홀점수'] = scorecard.iloc[:, 9:].sum(axis=1)
        summary['총점'] = summary['A홀점수'] + summary['B홀점수']

        st.write(summary)
        st.write(scorecard)

if __name__ == "__main__":
    app()
