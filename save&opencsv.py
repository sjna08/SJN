import pandas as pd
import streamlit as st

# 예시 데이터 생성
data = {
    'name': ['John', 'Anna', 'Peter', 'Linda'],
    'age': [28, 22, 35, 58]
}
df = pd.DataFrame(data)

# 데이터를 CSV 파일로 저장
df.to_csv('data.csv', index=False)

# 사용자에게 데이터를 불러올 것인지 묻기
response = st.text_input("CSV 파일을 불러올까요? (yes/no): ")

if response.lower() == 'yes':
    # 데이터 불러오기
    loaded_data = pd.read_csv('data.csv')
    st.write(loaded_data)
elif response.lower() == 'no':
    st.write("파일을 불러오지 않습니다.")
