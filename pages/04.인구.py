import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="인구 통계 분석", layout="wide")

# 데이터 로드
@st.cache_data
def load_data():
    # 파일 인코딩 문제 해결 (cp949 사용)
    df = pd.read_csv('population.csv', encoding='cp949')
    # 지역명 정제: '서울특별시 광진구 구의제3동(1121587000)' -> '구의제3동'
    df['지역'] = df['행정구역'].str.split('(').str[0].str.split(' ').str[-1]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 로드 중 오류 발생: {e}")
    st.stop()

st.title("📊 지역별 연령 인구 분포 시각화")

# 지역 선택
selected_region = st.selectbox("분석할 행정동을 선택하세요:", df['지역'].unique())

# 선택된 데이터 처리
region_data = df[df['지역'] == selected_region]

# '세'가 포함된 컬럼만 추출하여 나이별 데이터 생성
age_cols = [col for col in region_data.columns if '세' in col]
pop_values = region_data[age_cols].iloc[0].values

plot_df = pd.DataFrame({
    '나이': [int(col.replace('세', '')) for col in age_cols],
    '인구수': pop_values
})

# 그래프 생성
fig = px.line(plot_df, x='나이', y='인구수', 
              title=f"{selected_region} 연령별 인구 분포",
              markers=True) # 데이터 포인트 표시

# 무지개 색상 테마 적용 및 바탕 보라색 설정
fig.update_layout(
    plot_bgcolor='#4B0082',  # 바탕색 (보라색 계열)
    paper_bgcolor='#4B0082',
    font_color='white',
    title_font_color='white'
)

# 그래프 선 색상 변경 (무지개색 연출 - 포인트별 색상 다르게)
fig.update_traces(line=dict(color='cyan', width=3))

st.plotly_chart(fig, use_container_width=True)

# 데이터 확인용
if st.checkbox("데이터 테이블 보기"):
    st.write(region_data)
