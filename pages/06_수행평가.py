import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="일식 레시피 마스터", layout="wide")

# 다크 테마 디자인 (검정 배경 + 빨강/보라 포인트)
st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: #E0E0E0; }
    h1 { color: #FF4B4B; text-align: center; border-bottom: 2px solid #8A2BE2; }
    h2, h3 { color: #BB86FC; }
    .stSelectbox { color: #E0E0E0; }
    div[data-testid="stSuccess"] { background-color: #1E1E1E; border: 1px solid #FF4B4B; color: #FFDADA; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍣 일식 레시피 마스터 데이터베이스")
st.write("20가지 정통 일식 메뉴와 조리 팁을 기록한 포트폴리오입니다.")

# 20가지 일식 메뉴 데이터
data = {
    '메뉴명': [
        '연어 초밥', '규동', '미소 된장국', '가츠동', '덴푸라', 
        '오코노미야키', '타코야키', '우동', '소바', '스끼야끼',
        '나베야끼 우동', '야끼소바', '치킨 카라아게', '사케동', '낫또 비빔밥',
        '오니기리', '차완무시', '데리야끼 치킨', '아게다시 도후', '니쿠자가'
    ],
    '주재료': [
        '연어, 초밥용 밥', '소고기, 양파, 쯔유', '미소 된장, 다시마', '돈까스, 양파, 계란', '새우, 야채, 튀김가루',
        '밀가루, 양배추, 베이컨', '문어, 반죽', '우동면, 쯔유', '메밀면, 쯔유', '소고기, 대파, 배추',
        '우동면, 새우튀김, 버섯', '야끼소바면, 야채, 소스', '닭다리살, 전분', '연어, 덮밥용 밥', '낫또, 계란',
        '밥, 김, 참치', '계란, 다시물', '닭다리살, 데리야끼 소스', '두부, 전분, 쯔유', '소고기, 감자, 양파'
    ],
    '핵심 팁': [
        '밥의 온도를 체온과 비슷하게 맞추세요.', '소고기를 먼저 볶아 육즙을 가두세요.', '된장은 마지막에 풀어 향을 살리세요.', '돈까스가 눅눅해지지 않게 소스를 빠르게 끓이세요.', '튀김옷은 얼음물로 만들어야 바삭합니다.',
        '양배추를 듬뿍 넣어야 식감이 좋습니다.', '반죽을 듬뿍 넣고 굴리듯 익히세요.', '면을 삶은 뒤 찬물에 헹궈야 탄력이 생깁니다.', '메밀면은 짧은 시간에 삶아내세요.', '고기는 살짝 익혀 부드러움을 유지하세요.',
        '튀김은 마지막에 올려 바삭함을 살리세요.', '센 불에서 빠르게 볶아야 면이 불지 않습니다.', '이중 튀김을 하면 더욱 바삭해집니다.', '연어는 소금물에 살짝 담가 비린내를 제거하세요.', '낫또는 많이 저을수록 점성이 생겨 맛있습니다.',
        '삼각 모양을 잡을 때 손에 물을 묻히세요.', '계란물을 고운 체에 걸러야 매끄럽습니다.', '소스가 타지 않게 약불에서 조절하세요.', '두부 표면의 물기를 완전히 제거해야 바삭합니다.', '감자가 으스러지지 않게 천천히 조리하세요.'
    ]
}

df = pd.DataFrame(data)

# 메뉴 선택
selected_dish = st.selectbox("학습할 일식 메뉴를 선택하세요:", df['메뉴명'])

# 정보 표시
if selected_dish:
    dish_info = df[df['메뉴명'] == selected_dish].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 메뉴 정보")
        st.write(f"**주요 식재료:** {dish_info['주재료']}")
    
    with col2:
        st.subheader("💡 셰프의 핵심 팁")
        st.success(dish_info['핵심 팁'])

st.markdown("---")
st.markdown("<p style='text-align: center; color: #555;'>조리과 수행평가 데이터 아카이브 | 2026.06.11</p>", unsafe_allow_html=True)
