죄송합니다, 제가 올바르게 코드를 작성하지 않았습니다. Python은 indentation을 매우 엄격하게 취급하는 언어입니다. 주석에 쓰인 `#...`은 실제 코드로 대체되어야 하는 부분을 나타내는 데 사용된 것입니다. 여기서 `제출` 버튼이 클릭되었을 때 실행되어야 하는 코드를 넣어야 합니다. 아래에 수정된 코드를 제공하겠습니다.

```python
# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd
import base64
import io

# Main Page
st.title("ParkGolf ScoreCard")

# 홀 이름과 거리 설정
holes = ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 
         # ... (추가로 필요한 홀들)
        ]

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
else:
    st.session_state['scorecard'].index = players  # update player names in scorecard
scorecard = st.session_state['scorecard']

# 사용자에게 입력 받기
for hole in selected_holes:
    st.subheader(hole)
    for player in players:
        scorecard.loc[player, hole] = st.number_input(f'{player} {hole} 점수', min_value=0, value=0, key=f'{player}_{hole}')

# 입력 받은 정보를 표시하고 다운로드 받기
if st.button('제출'):
    # 작업을 계속하기 전에 결과를 계산하고 출력하는 실제 코드를 여기에 작성해야 합니다.
    pass
```
위 코드의 마지막 부분에서 '제출' 버튼이 클릭되었을 때 수행해야 하는 작업을 추가하시면 됩니다. 이 경우에는 플레이어의 점수를 계산하고 결과를 출력하는 코드를 추가해야 합니다.
