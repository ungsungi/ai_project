import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 페이지 설정
st.set_page_config(page_title="인구 통계 분석", layout="wide")

# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv('population.csv', encoding='cp949')
    
    # [핵심 수정] 쉼표 제거 및 숫자형 변환
    # '세'가 들어간 모든 컬럼을 찾아 숫자로 변환
    age_cols = [col for col in df.columns if '세' in col]
    for col in age_cols:
        # 데이터가 문자열일 경우 쉼표 제거 후 숫자로 변환
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '').astype(float)
    
    # 지역명 정리
    df['지역'] = df['행정구역'].str.split('(').str[0].str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 로드 중 오류 발생: {e}")
    st.stop()

st.title("📊 인구 데이터 시각화 및 분석")

# 연령대 선택
age_cols = [col for col in df.columns if '세' in col]
# 컬럼명에서 숫자만 추출하여 정렬
age_numbers = sorted(list(set([int(re.findall(r'\d+', col)[-1]) for col in age_cols])))

selected_age = st.slider("분석할 연령대를 선택하세요:", 0, max(age_numbers), 20)

# 선택한 연령에 해당하는 컬럼 찾기
# '10세' 등을 정규표현식으로 정확히 매칭
def get_target_col(age):
    for col in age_cols:
        if int(re.findall(r'\d+', col)[-1]) == age:
            return col
    return None

target_col = get_target_col(selected_age)

if target_col:
    # 데이터 정렬 (상위 10개)
    top_regions = df.nlargest(10, target_col)

    # 그래프 그리기
    st.subheader(f"🔍 {selected_age}세 인구가 가장 많은 지역 Top 10")

    fig = px.bar(top_regions, x='지역', y=target_col, 
                 title=f"{selected_age}세 인구 분포 현황",
                 color=target_col, 
                 color_continuous_scale='Rainbow')

    fig.update_layout(
        plot_bgcolor='#4B0082',
        paper_bgcolor='#4B0082',
        font_color='white',
        title_font_color='white'
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("해당 연령대의 데이터를 찾을 수 없습니다.")

if st.checkbox("전체 데이터 보기"):
    st.write(df)
