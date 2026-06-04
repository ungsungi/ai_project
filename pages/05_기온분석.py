import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="서울 기온 분석 및 예측", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8")
    df.columns = ["날짜", "지점", "평균기온", "최저기온", "최고기온"]
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str).str.strip(), errors='coerce')
    return df.dropna(subset=['날짜'])

df = load_data()

st.title("🌡️ 서울 기온 분석 및 미래 예측")

# 탭 구성
tab1, tab2 = st.tabs(["과거 데이터 분석", "미래 기온 예측"])

with tab1:
    selected_date = st.date_input("날짜를 선택하세요", df["날짜"].max().date())
    year = selected_date.year
    year_df = df[df["날짜"].dt.year == year]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=year_df["날짜"], y=year_df["최고기온"], name="최고기온", line=dict(color="#FFD700", width=3)))
    fig.add_trace(go.Scatter(x=year_df["날짜"], y=year_df["최저기온"], name="최저기온", line=dict(color="#FF0000", width=3)))
    fig.update_layout(title=f"{year}년 기온", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🔮 미래 연도 기온 예측")
    target_year = st.number_input("예측하고 싶은 연도를 입력하세요", min_value=2027, max_value=2100, value=2027)
    
    if st.button("예측 시작"):
        # 연도별 평균 기온 추세 학습
        df['연도'] = df['날짜'].dt.year
        yearly_avg = df.groupby('연도')[['최고기온', '최저기온']].mean().reset_index()
        
        X = yearly_avg[['연도']]
        y_max = yearly_avg['최고기온']
        y_min = yearly_avg['최저기온']
        
        model_max = LinearRegression().fit(X, y_max)
        model_min = LinearRegression().fit(X, y_min)
        
        pred_max = model_max.predict([[target_year]])[0]
        pred_min = model_min.predict([[target_year]])[0]
        
        st.success(f"{target_year}년 예측 결과")
        col1, col2 = st.columns(2)
        col1.metric("예측 최고기온", f"{pred_max:.2f}℃")
        col2.metric("예측 최저기온", f"{pred_min:.2f}℃")
        st.info("※ 이 예측은 과거 데이터의 선형 회귀 분석 결과입니다.")
