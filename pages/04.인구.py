import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 페이지 설정
st.set_page_config(page_title="인구 통계 분석", layout="wide")

# 데이터 로드
@st.cache_data
def load_data():
    # 한글 인코딩 문제 해결을 위해 cp949 사용
    df = pd.read_csv('population.csv', encoding='cp949')
    
    # '행정구역' 데이터 정제 (괄호 제거 및 공백 정리)
    df['지역'] = df['행정구역'].str.split('(').str[0].str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 로드 중 오류 발생: {e}")
    st.stop()

st.title("📊 지역별 연령 인구 분포 시각화")

# 지역 선택
selected_region = st.selectbox("분석할 행정동을 선택하세요:", df['지역'].unique())

# 선택된 데이터 필터링
region_data = df[df['지역'] == selected_region]

# '세'가 포함된 컬럼만 추출 (정규표현식 활용)
# 컬럼명에 '세'가 포함된 모든 열을 찾습니다.
age_cols = [col for col in region_data.columns if '세' in col]

# 나이 추출 함수: 2026년04월_거주자_10세 -> 10으로 변환
def extract_age(col_name):
    numbers = re.findall(r'\d+', col_name)
    return int(numbers[-1]) if numbers else 0

# 데이터 프레임 구성
pop_values = region_data[age_cols].iloc[0].values
plot_df = pd.DataFrame({
    '나이': [extract_age(col) for col in age_cols],
    '인구수': pop_values
})

# 그래프 생성
fig = px.line(plot_df, x='나이', y='인구수', 
              title=f"{selected_region} 연령별 인구 분포",
              markers=True)

# 바탕 보라색 및 스타일 설정
fig.update_layout(
    plot_bgcolor='#4B0082',  # 보라색 배경
    paper_bgcolor='#4B0082',
    font_color='white',
    title_font_color='white'
)

# 그래프 선 색상 (무지개색 느낌을 위해 선을 밝은색으로 설정)
fig.update_traces(line=dict(color='#00FFFF', width=3)) # 시안색(하늘색)으로 가시성 확보

st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블 표시
if st.checkbox("데이터 상세 보기"):
    st.write(region_data)
