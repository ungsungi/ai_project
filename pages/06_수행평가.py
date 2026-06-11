import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="일식 레시피 아카이브", layout="wide")

# 보라색/빨간색 디자인 테마
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    h1 { color: #8B0000; text-align: center; border-bottom: 3px solid #6D28D9; }
    .stButton>button { background-color: #6D28D9; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍣 일식 레시피 아카이브")
st.write("전문 일식 요리 과정과 핵심 포인트를 정리한 페이지입니다.")

# 일식 데이터
data = {
    '메뉴명': ['연어 초밥', '규동 (소고기 덮밥)', '미소 된장국', '가츠동 (돈까스 덮밥)'],
    '주재료': ['연어, 식초 밥', '소고기, 양파, 달걀', '미소 된장, 다시마, 두부', '돈까스, 양파, 달걀'],
    '핵심 팁': ['밥의 온도가 체온과 비슷할 때 연어를 올리세요.', '소고기를 볶을 때 설탕을 먼저 넣으면 풍미가 살아납니다.', '된장은 마지막에 풀어야 향이 날아가지 않습니다.', '돈까스의 바삭함을 위해 소스를 빠르게 끓여 붓습니다.'],
    '난이도': ['중', '하', '하', '중']
}
df = pd.DataFrame(data)

# 메뉴 선택
selected_dish = st.selectbox("학습할 일식 메뉴를 선택하세요:", df['메뉴명'])

# 정보 표시
if selected_dish:
    dish_info = df[df['메뉴명'] == selected_dish].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 기본 정보")
        st.write(f"**주요 식재료:** {dish_info['주재료']}")
        st.write(f"**난이도:** {dish_info['난이도']}")
    
    with col2:
        st.subheader("💡 셰프의 핵심 팁")
        st.success(dish_info['핵심 팁'])

st.markdown("---")
st.write("※ 이 웹사이트는 조리 전공 수행평가를 위한 레시피 기록용 앱입니다.")
