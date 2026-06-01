import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('population.csv')
    return df

df = load_data()

# 데이터 전처리: '행정구역'에서 동 이름만 추출
df['지역'] = df['행정구역'].str.split('(').str[0]

st.title("지역별 인구 분포 시각화")

# 지역 선택
selected_region = st.selectbox("행정구를 선택하세요:", df['지역'].unique())

# 선택된 데이터 필터링 (0세부터 100세 이상까지의 컬럼 추출)
region_data = df[df['지역'] == selected_region]
age_cols = [col for col in region_data.columns if '세' in col]
pop_values = region_data[age_cols].iloc[0].values

plot_df = pd.DataFrame({
    '나이': [i for i in range(len(pop_values))],
    '인구수': pop_values
})

# 그래프 그리기
fig = px.line(plot_df, x='나이', y='인구수', title=f"{selected_region} 연령별 인구 분포")

# 그래프 스타일 설정
fig.update_layout(
    plot_bgcolor='purple',  # 바탕 보라색
    paper_bgcolor='purple',
    font_color='white'
)

# 무지개색 라인 설정 (Plotly 기본 테마 혹은 사용자 지정 색상)
fig.update_traces(line=dict(color='yellow', width=3)) 
# 참고: 선 색상을 무지개색으로 그라데이션 하려면 scatter gl 사용이 권장되나, 
# 간단한 꺾은선은 위와 같이 설정 가능합니다.

st.plotly_chart(fig)
