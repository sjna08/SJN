# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd

# Streamlit 앱 시작
def app():
    # 플레이어 수 설정
    num_players = 4
    players = [st.sidebar.text_input(f'Player {i+1} 이름', value=f'Player {i+1}') for i in range(num_players)]

    # 홀 수 설정
    holes = ['A' + str(i) for i in range(1, 10)] + ['B' + str(i) for i in range(1, 10)]

    # 스코어카드 생성
    scorecard = pd.DataFrame(index=players, columns=holes)

    # 사용자에게 입력 받기
    for hole in holes:
        st.subheader(hole)
        for player in players:
            scorecard.loc[player, hole] = st.number_input(f'{player} {hole} 점수', min_value=0, value=0, key=f'{player}_{hole}')

    # 입력 받은 정보를 표시하기
    if st.button('제출'):
        scorecard['전반 점수'] = scorecard.iloc[:, :9].sum(axis=1)
        scorecard['후반 점수'] = scorecard.iloc[:, 9:18].sum(axis=1)
        scorecard['총점'] = scorecard['전반 점수'] + scorecard['후반 점수']

        st.write(scorecard)

if __name__ == "__main__":
    app()
