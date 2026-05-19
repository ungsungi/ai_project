import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="서울 관광지 가이드", layout="wide")

st.title("🌏 외국인이 사랑하는 서울의 주요 관광지 TOP 10")

# 관광지 데이터 (위도, 경도, 이름, 지하철역, 설명)
tour_spots = [
    {"name": "경복궁", "coords": [37.5796, 126.9770], "station": "경복궁역", "info": "조선의 법궁으로, 고풍스러운 전통 건축미를 느낄 수 있습니다."},
    {"name": "북촌한옥마을", "coords": [37.5828, 126.9836], "station": "안국역", "info": "전통 한옥이 밀집한 곳으로, 서울의 과거와 현재가 공존하는 거리입니다."},
    {"name": "명동", "coords": [37.5635, 126.9840], "station": "명동역", "info": "한국의 대표적인 쇼핑과 미식의 거리로, 언제나 활기가 넘칩니다."},
    {"name": "남산서울타워", "coords": [37.5512, 126.9882], "station": "명동역/회현역", "info": "서울의 랜드마크로, 정상에서 서울의 야경을 한눈에 조망할 수 있습니다."},
    {"name": "인사동", "coords": [37.5732, 126.9860], "station": "종각역/안국역", "info": "전통 공예품과 갤러리가 가득하며, 한국적인 기념품을 사기에 좋습니다."},
    {"name": "동대문디자인플라자(DDP)", "coords": [37.5668, 127.0096], "station": "동대문역사문화공원역", "info": "독특한 디자인의 건축물로, 전시와 패션 이벤트가 자주 열립니다."},
    {"name": "홍대 거리", "coords": [37.5568, 126.9238], "station": "홍대입구역", "info": "젊음과 예술의 거리로, 버스킹과 맛집, 클럽 문화가 유명합니다."},
    {"name": "강남역", "coords": [37.4979, 127.0276], "station": "강남역", "info": "현대적인 서울의 중심지로, 대형 쇼핑몰과 카페가 즐비합니다."},
    {"name": "이태원", "coords": [37.5348, 126.9943], "station": "이태원역", "info": "다양한 국가의 음식과 이국적인 문화를 즐길 수 있는 자유로운 곳입니다."},
    {"name": "롯데월드타워", "coords": [37.5126, 127.1025], "station": "잠실역", "info": "대한민국 최고층 건물로, 쇼핑, 전망대, 아쿠아리움을 모두 즐길 수 있습니다."}
]

# 지도 생성 (서울 중심 좌표)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for spot in tour_spots:
    folium.Marker(
        location=spot["coords"],
        popup=f"<b>{spot['name']}</b><br>가까운 역: {spot['station']}",
        tooltip=spot["station"],
        icon=folium.Icon(color="beige", icon="info-sign") # 노란색 계열 마커
    ).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=900, height=500)

# 하단 정보 설명
st.subheader("📍 관광지 상세 정보")
for spot in tour_spots:
    with st.expander(f"{spot['name']} (지하철: {spot['station']})"):
        st.write(f"**놀거리/특징:** {spot['info']}")
