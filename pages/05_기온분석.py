import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

# 데이터 읽기
try:
    df = pd.read_csv("seoul.csv", encoding="cp949")
except:
    df = pd.read_csv("seoul.csv", encoding="utf-8")

# 컬럼명 수정
df.columns = ["날짜", "지점", "평균기온", "최저기온", "최고기온"]

# [수정] 날짜 데이터 전처리 및 변환
# 데이터 타입이 문자열이 아닐 경우 대비하여 형변환 후 공백 제거
df["날짜"] = df["날짜"].astype(str).str.strip()

# format을 명시하지 않으면 자동으로 형식을 찾지만, 
# 데이터가 섞여있을 경우 errors='coerce'를 사용하여 변환 불가능한 값은 NaT로 처리
df["날짜"] = pd.to_datetime(df["날짜"], errors='coerce')

# 변환 실패한 데이터(NaT) 제거
df = df.dropna(subset=['날짜'])

# 날짜 선택
selected_date = st.date_input(
    "날짜를 선택하세요",
    value=df["날짜"].max().date(),
    min_value=df["날짜"].min().date(),
    max_value=df["날짜"].max().date()
)

# 선택한 날짜 정보
selected_row = df[df["날짜"].dt.date == selected_date]

if not selected_row.empty:
    row = selected_row.iloc[0]

    st.subheader(f"📅 {selected_date}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("최고기온", f"{row['최고기온']}℃")
    with col2:
        st.metric("최저기온", f"{row['최저기온']}℃")

    # 선택한 날짜가 속한 연도
    year = selected_date.year
    year_df = df[df["날짜"].dt.year == year]

    # 그래프 생성
    fig = go.Figure()

    # 최고기온
    fig.add_trace(go.Scatter(
        x=year_df["날짜"], y=year_df["최고기온"],
        mode="lines", name="최고기온",
        line=dict(color="#FFFF00", width=3)
    ))

    # 최저기온
    fig.add_trace(go.Scatter(
        x=year_df["날짜"], y=year_df["최저기온"],
        mode="lines", name="최저기온",
        line=dict(color="#FF0000", width=3)
    ))

    # 선택 날짜 표시
    fig.add_vline(x=selected_date, line_dash="dash")

    fig.update_layout(
        title=f"{year}년 서울 최고·최저기온 변화",
        xaxis_title="날짜",
        yaxis_title="기온 (℃)",
        hovermode="x unified",
        showlegend=True,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("해당 날짜 데이터가 없습니다.")
