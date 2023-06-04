import streamlit as st
import pandas as pd
import base64
import io

def app():
    players = ['Player1', 'Player2', 'Player3', 'Player4']
    holes = ['A1_Par4(60m)', 'A2_Par3(40m)', 'A3_Par3(65m)', 'A4_Par4(100m)', 'A5_Par5(130m)', 'A6_Par4(72m)', 'A7_Par4(81m)', 'A8_Par3(50m)', 'A9_Par3(50m)', 'B1_Par3(69m)', 'B2_Par4(100m)', 'B3_Par4(68m)', 'B4_Par3(50m)', 'B5_Par4(58m)', 'B6_Par3(55m)', 'B7_Par4(71m)', 'B8_Par5(123m)', 'B9_Par3(66m)']

    # Create a dictionary to keep the scores
    scorecard = {player: {} for player in players}

    for player in players:
        st.sidebar.header(player)
        for hole in holes:
            scorecard[player][hole] = st.sidebar.number_input(f'{player} {hole} Score', min_value=0, value=0)

    if st.button('Submit'):
        scorecard_df = pd.DataFrame(scorecard)

        # Calculate totals
        total = scorecard_df.sum().rename('Total')
        scorecard_df = scorecard_df.append(total)

        A_total = scorecard_df[holes[:9]].sum(axis=1).rename('A Total')
        B_total = scorecard_df[holes[9:]].sum(axis=1).rename('B Total')

        scorecard_df = pd.concat([scorecard_df, A_total, B_total], axis=1)

        st.write(scorecard_df.T)

        csv = scorecard_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)


app()
