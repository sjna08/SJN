import streamlit as st
import pandas as pd
import base64
import io

st.title("ParkGolf ScoreCard")

def app():

    num_players = 4
    players = [st.sidebar.text_input(f'Player {i+1}이름',value=f'Player{i+1}') for i in range(num_players)]
  
    page = st.sidebar.radio('페이지 선택', ['A 홀', 'B 홀', 'C 홀', 'D 홀', '전체'])

    holes = {
        'A 홀': ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)'],
        'B 홀': ['B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)'],
        'C 홀': ['C1_Par4(60m)', 'C2_Par3(40m)', 'C3_Par3(65m)', 'C4_Par4(100m)', 'C5_Par5(130m)', 'C6_Par4(72m)', 'C7_Par4(81m)', 'C8_Par3(50m)', 'C9_Par3(50m)'],
        'D 홀': ['D1_Par3(69m)', 'D2_Par4(100m)', 'D3_Par4(68m)', 'D4_Par3(50m)', 'D5_Par4(58m)', 'D6_Par3(55m)', 'D7_Par4(71m)', 'D8_Par5(123m)', 'D9_Par3(66m)'],
        '전체': ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)',
                 'B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)',
                 'C1_Par4(60m)', 'C2_Par3(40m)', 'C3_Par3(65m)', 'C4_Par4(100m)', 'C5_Par5(130m)', 'C6_Par4(72m)', 'C7_Par4(81m)', 'C8_Par3(50m)', 'C9_Par3(50m)',
                 'D1_Par3(69m)', 'D2_Par4(100m)', 'D3_Par4(68m)', 'D4_Par3(50m)', 'D5_Par4(58m)', 'D6_Par3(55m)', 'D7_Par4(71m)', 'D8_Par5(123m)', 'D9_Par3(66m)']
    }

    if page == '전체':
        selected_holes = holes['전체']
    else:
        selected_holes = holes[page]

    scorecard = pd.DataFrame(index=players, columns=selected_holes)

    if page.startswith('A'):
        if 'scorecard' not in st.session_state:
            st.session_state['scorecard'] = scorecard

    for hole in selected_holes:
        st.subheader(hole)
        for player in players:
            default_value = 0 if not pd.isna(st.session_state['scorecard'].loc[player, hole]) else st.session_state['scorecard'].loc[player, hole]
            score = st.number_input(f'{player} {hole} 점수', min_value=0, value=int(default_value), key=f'{player}_{hole}', format="%d")
            st.session_state['scorecard'].loc[player, hole] = score

    if st.button('제출'):
        summary = pd.DataFrame(index=players, columns=['TTL', 'A', 'B', 'A_Dif', 'B_Dif', 'C', 'D', 'C_Dif', 'D_Dif', 'TTL_Dif'])
        summary['A'] = st.session_state['scorecard'].iloc[:, :9].sum(axis=1)
        summary['B'] = st.session_state['scorecard'].iloc[:, 9:18].sum(axis=1)
        summary['C'] = st.session_state['scorecard'].iloc[:, 18:27].sum(axis=1)
        summary['D'] = st.session_state['scorecard'].iloc[:, 27:].sum(axis=1)
        summary['TTL'] = summary['A'] + summary['B'] + summary['C'] + summary['D']
        summary['A_Dif'] = summary['A'] - 33
        summary['B_Dif'] = summary['B'] - 33
        summary['C_Dif'] = summary['C'] - 33
        summary['D_Dif'] = summary['D'] - 33
        summary['TTL_Dif'] = summary['TTL'] - 132

        st.write(summary)
        st.write(st.session_state['scorecard'])

        full_scorecard = pd.concat([summary, st.session_state['scorecard']], axis=1)

        csv_buffer = io.StringIO()
        full_scorecard.astype(int).to_csv(csv_buffer, index=True, encoding='utf-8-sig')
        csv_string = csv_buffer.getvalue()
        b64 = base64.b64encode(csv_string.encode()).decode() 
        href = f'<a href="data:file/csv;base64,{b64}" download="scorecard.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

        if st.button("점수카드 저장"):
            with open('scorecard.csv', 'w') as f:
                f.write(csv_string)

if __name__ == "__main__":
    app()
