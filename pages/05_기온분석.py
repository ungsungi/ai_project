import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="서울 기온 그래프", layout="wide")

st.title("🌡️ 서울 기온 조회")

# 데이터 불러오기
df = pd.read_csv("seoul.csv", encoding="cp949")

# 컬럼명 정리
df.columns = ['날짜', '지점', '평균기온', '최저기온', '최고기온']

# 날짜형 변환
df['날짜'] = pd.to_datetime(df['날짜'])

# 날짜 선택
selected_date = st.date_input(
    "날짜를 선택하세요",
    value=df['날짜'].max().date(),
    min_value=df['날짜'].min().date(),
    max_value=df['날짜'].max().date()
)

# 선택한 날짜 데이터
result = df[df['날짜'].dt.date == selected_date]

if len(result) > 0:
    row = result.iloc[0]

    st.subheader(f"📅 {selected_date}")

    st.write(f"최고기온: **{row['최고기온']}℃**")
    st.write(f"최저기온: **{row['최저기온']}℃**")

    # 그래프
    fig, ax = plt.subplots(figsize=(8, 5))

    x = ['기온']

    ax.plot(
        x,
        [row['최고기온']],
        color='#FFFF00',   # 샛노란색
        marker='o',
        linewidth=3,
        label='최고기온'
    )

    ax.plot(
        x,
        [row['최저기온']],
        color='#FF0000',   # 새빨간색
        marker='o',
        linewidth=3,
        label='최저기온'
    )

    ax.set_ylabel("기온 (℃)")
    ax.set_title(f"{selected_date} 기온")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

else:
    st.error("해당 날짜의 데이터가 없습니다.")
