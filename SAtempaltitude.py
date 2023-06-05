import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 프레임 만들기
data = {
    'City': ['Lima', 'Cusco', 'La Paz', 'Uyuni', 'Buenos Aires', 'Puerto Iguazu', 'El Calafate', 'Rio de Janeiro'],
    'Country': ['Peru', 'Peru', 'Bolivia', 'Bolivia', 'Argentina', 'Argentina', 'Argentina', 'Brazil'],
    'Altitude (m)': [0, 3399, 3640, 3656, 25, 196, 201, 0],
    'Avg Temp (C)': [(20+30)/2, (3+21)/2, (3+21)/2, (3+21)/2, (17+28)/2, (21+32)/2, (7+19)/2, (23+30)/2],
    'Days': [(2,3), (4,9), (10,12), (13,15), (16,18,30), (19,21), (22,25), (26,29)]
}

df = pd.DataFrame(data)

# 그래프 그리기
fig, ax1 = plt.subplots()

sns.lineplot(data=df, x='City', y='Altitude (m)', sort=False, ax=ax1)
ax2 = ax1.twinx()
sns.lineplot(data=df, x='City', y='Avg Temp (C)', sort=False, color='r', ax=ax2)

plt.show()
