import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="서울 기온 분석", page_icon="🌡️", layout="wide")

st.title("🌡️ 서울 기온 분석")

# 데이터 로딩
@st.cache_data
def load_data():
    try:
        # 데이터가 클 경우를 대비해 engine='python' 사용
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8")
    
    # 컬럼명 정리
    df.columns = ["날짜", "지점", "평균기온", "최저기온", "최고기온"]
    
    # 날짜 데이터 정제 (공백 제거 후 datetime 변환)
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str).str.strip(), errors='coerce')
    return df.dropna(subset=['날짜'])

df = load_data()

# 날짜 선택 위젯 (해당 연도의 전체 데이터를 보여주기 위해 연도 선택 가능)
st.sidebar.header("조회 설정")
selected_date = st.date_input(
    "날짜를 선택하세요",
    value=df["날짜"].max().date(),
    min_value=df["날짜"].min().date(),
    max_value=df["날짜"].max().date()
)

# 데이터 필터링
year = selected_date.year
year_df = df[df["날짜"].dt.year == year].copy()

# 선택한 특정 날짜 정보 추출
selected_row = df[df["날짜"].dt.date == selected_date]

if not selected_row.empty:
    r = selected_row.iloc[0]
    st.subheader(f"📅 {selected_date} 기온 정보")
    
    # 메트릭 표시
    c1, c2 = st.columns(2)
    c1.metric("최고기온", f"{r['최고기온']}℃")
    c2.metric("최저기온", f"{r['최저기온']}℃")

    # 그래프 생성
    fig = go.Figure()

    # 1. 최고기온 (샛노란색)
    fig.add_trace(go.Scatter(
        x=year_df["날짜"], y=year_df["최고기온"],
        mode="lines", name="최고기온",
        line=dict(color="#FFD700", width=3) # 샛노란색 (Gold)
    ))

    # 2. 최저기온 (새빨간색)
    fig.add_trace(go.Scatter(
        x=year_df["날짜"], y=year_df["최저기온"],
        mode="lines", name="최저기온",
        line=dict(color="#FF0000", width=3) # 새빨간색
    ))

    # 선택한 날짜 위치에 세로선 표시
    fig.add_vline(x=pd.Timestamp(selected_date), line_dash="dash", line_color="gray")

    # 레이아웃 업데이트
    fig.update_layout(
        title=f"{year}년 서울 기온 변화",
        xaxis_title="날짜 (월/일)",
        yaxis_title="기온 (℃)",
        hovermode="x unified",
        showlegend=True, # 범례 표시
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.5)"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("선택하신 날짜의 데이터를 불러올 수 없습니다.")
