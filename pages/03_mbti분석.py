import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()
mbti_types = df.columns[1:]

st.title("🌍 MBTI 글로벌 데이터 탐색기")

# 사이드바에서 모드 선택
mode = st.sidebar.radio("분석 모드를 선택하세요:", ["국가별 분포 보기", "유형별 상위 국가 보기"])

if mode == "국가별 분포 보기":
    st.header("국가별 MBTI 유형 분포")
    selected_country = st.selectbox("국가를 선택하세요:", df['Country'].unique())
    
    country_data = df[df['Country'] == selected_country].iloc[0, 1:].sort_values(ascending=False)
    
    # 색상 로직: 1등은 빨강, 나머지는 그라데이션 회색
    colors = ['rgba(255, 65, 54, 0.9)'] + [f'rgba(128, 128, 128, {max(0.1, 0.7 - (i/16)*0.5)})' for i in range(1, 16)]
    
    fig = go.Figure(data=[go.Bar(x=country_data.index, y=country_data.values, marker_color=colors)])
    fig.update_layout(title=f"{selected_country}의 MBTI 유형 분포", template="plotly_white")
    st.plotly_chart(fig)

else:
    st.header("유형별 상위 10개 국가")
    selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_types)
    
    top_10 = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)
    
    # 색상 로직: 1등은 빨강, 나머지는 회색
    colors = ['rgba(255, 65, 54, 0.9)'] + ['rgba(128, 128, 128, 0.6)'] * 9
    
    fig = go.Figure(data=[go.Bar(x=top_10['Country'], y=top_10[selected_mbti], marker_color=colors)])
    fig.update_layout(title=f"'{selected_mbti}' 비율이 높은 상위 10개 국가", template="plotly_white")
    st.plotly_chart(fig)
