# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd
import base64
import io

# Main Page
st.title("ParkGolf ScoreCard")
# Streamlit 앱 시작
def app():
# 홀 이름과 거리 설정
holes = ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 
         'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)', 
         'B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 
         'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)']

    # 플레이어 수 설정
    num_players = 4
    players = [st.sidebar.text_input(f'Player {i+1}이름',value=f'Player{i+1}') for i in range(num_players)]
  
    for i, player in enumerate(players):
      for hole in holes:
          key = f"{player}_{hole}_{i}"  # player index 추가
          scorecard.loc[player, hole] = st.number_input(f'{player} {hole} 점수', min_value=0, value=0, key=key)


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

    # 입력 받은 정보를 표시하고 다운로드 받기
    if st.button('제출'):
        summary = pd.DataFrame(index=players, columns=['TTL','A','B', 'A_Dif','B_Dif','TTL_Dif'])
        summary['A'] = scorecard.iloc[:, :9].sum(axis=1)
        summary['B'] = scorecard.iloc[:, 9:].sum(axis=1)
        summary['TTL'] = summary['A'] + summary['B']

         def app():
    # 홀 이름과 거리 설정
    holes = ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 
             'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)', 
             'B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 
             'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)']

    
        # 차이를 계산
        summary['A_Dif'] = summary['A'] - 33
        summary['B_Dif'] = summary['B'] - 33
        summary['TTL_Dif'] = summary['TTL'] - 66

        st.write(summary)
        st.write(scorecard)

        # 스코어카드와 요약을 합치기
        full_scorecard = pd.concat([summary, scorecard], axis=1)

        csv_buffer = io.StringIO()
        full_scorecard.to_csv(csv_buffer, index=True, encoding='utf-8-sig')
        csv_string = csv_buffer.getvalue()
        b64 = base64.b64encode(csv_string.encode()).decode() 
        href = f'<a href="data:file/csv;base64,{b64}" download="scorecard.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
