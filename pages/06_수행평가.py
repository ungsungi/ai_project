import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 디자인 (보라색/빨간색 테마)
st.set_page_config(page_title="AI 요리 밸런스 분석기", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    h1 {
        color: #6D28D9; /* 보라색 */
        text-align: center;
        font-family: 'Nanum Gothic', sans-serif;
    }
    .stButton>button {
        background-color: #DC2626; /* 빨간색 */
        color: white;
        border-radius: 10px;
    }
    .stSlider [data-baseweb="slider"] {
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바 - 요리 정보 입력
st.sidebar.header("👨‍🍳 요리 정보 입력")
dish_name = st.sidebar.text_input("요리 이름", "오늘의 요리")
chef_name = st.sidebar.text_input("작성자(이름)", "학생성명")
dish_type = st.sidebar.selectbox("카테고리", ["한식", "양식", "중식", "일식", "디저트"])

st.sidebar.markdown("---")
st.sidebar.write("각 미각의 강도를 0~10점으로 조절하세요.")

# 3. 메인 화면 구성
st.title(f"🍴 {dish_name} 밸런스 분석")
st.write(f"**셰프:** {chef_name} | **카테고리:** {dish_type}")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 미각 데이터 입력")
    sweet = st.slider("🍭 단맛 (Sweetness)", 0, 10, 5)
    salty = st.slider("🧂 짠맛 (Saltiness)", 0, 10, 5)
    sour = st.slider("🍋 신맛 (Sourness)", 0, 10, 5)
    bitter = st.slider("☕ 쓴맛 (Bitterness)", 0, 10, 2)
    umami = st.slider("🍄 감칠맛 (Umami)", 0, 10, 7)

    # 데이터 프레임 생성
    df = pd.DataFrame(dict(
        r=[sweet, salty, sour, bitter, umami],
        theta=['단맛', '짠맛', '신맛', '쓴맛', '감칠맛']
    ))

with col2:
    st.subheader("📈 미각 레이더 차트")
    # 레이더 차트 시각화 (보라색 테두리, 빨간색 채우기)
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', line_color='#6D28D9', fillcolor='rgba(220, 38, 38, 0.4)')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 4. 분석 결과 출력 (간단한 로직)
st.subheader("📝 셰프의 분석 코멘트")

comments = []
if sweet > 7: comments.append("단맛이 강하여 아이들이 좋아할 것 같습니다.")
if salty > 7: comments.append("간이 센 편이므로 밥이나 빵과 곁들여주세요.")
if sour > 7: comments.append("산미가 좋아 전채 요리로 적합합니다.")
if umami > 7: comments.append("깊은 맛이 느껴지는 훌륭한 조화입니다.")
if not comments: comments.append("전체적으로 균형이 잘 잡힌 요리입니다.")

for comment in comments:
    st.write(f"- {comment}")

# 푸터
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: grey; font-size: 0.8em;">
        2024 요리 교과 수행평가 결과물 - Streamlit & GitHub 연동 프로젝트
    </div>
    """, unsafe_allow_html=True)
