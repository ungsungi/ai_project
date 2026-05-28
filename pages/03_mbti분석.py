import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()
mbti_types = df.columns[1:] # Country 제외한 유형 목록

st.title("🌍 국가별 MBTI 분포 시각화")

# 국가 선택
selected_country = st.selectbox("국가를 선택하세요:", df['Country'].unique())

# 데이터 추출 및 정렬
country_data = df[df['Country'] == selected_country].iloc[0, 1:]
sorted_data = country_data.sort_values(ascending=False)

# 색상 로직: 1등은 무지개(빨강 계열), 나머지는 회색 그라데이션
colors = []
for i in range(len(sorted_data)):
    if i == 0:
        colors.append('rgba(255, 65, 54, 0.9)')  # 1등: 강렬한 빨강/무지개 포인트
    else:
        # 나머지는 회색조 (1등과 멀어질수록 점점 흐리게)
        opacity = max(0.1, 0.7 - (i / len(sorted_data)) * 0.5)
        colors.append(f'rgba(128, 128, 128, {opacity})')

# 그래프 그리기
fig = go.Figure(data=[go.Bar(
    x=sorted_data.index,
    y=sorted_data.values,
    marker_color=colors
)])

fig.update_layout(
    title=f"{selected_country}의 MBTI 유형 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white"
)

st.plotly_chart(fig)
