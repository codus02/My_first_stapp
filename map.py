import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# 데이터 로드 및 전처리
birth_rate_file = data/연령별_출산율_및_합계출산율_행정구역별__20241120143517.csv
geojson_file = "C:/Users/chaet/Downloads/data/gdf_korea_sido_2022.json"

# 출생률 데이터
birth_rate_data = pd.read_csv(birth_rate_file, header=1, encoding='cp949')
birth_rate_data.rename(columns={'행정구역별': '행정구역', '합계출산율 (가임여성 1명당 명)': '출생률'}, inplace=True)
birth_rate_data = birth_rate_data[birth_rate_data['행정구역'] != '전국']
birth_rate_data = birth_rate_data[['행정구역', '출생률']]

# 지역 필터
valid_regions = [
    '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
    '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도',
    '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'
]
birth_rate_data = birth_rate_data[birth_rate_data['행정구역'].isin(valid_regions)]

# GeoJSON 데이터
geo_data = gpd.read_file(geojson_file)
geo_data = geo_data[['geometry', 'CTP_KOR_NM']]
geo_data.rename(columns={'CTP_KOR_NM': '행정구역'}, inplace=True)

# 데이터 병합
merged_data = geo_data.merge(birth_rate_data, how='inner', on='행정구역')
merged_data_geojson = merged_data.to_json()

# Streamlit 애플리케이션
st.title("전국 출생률 Choropleth 지도")
st.write("이 애플리케이션은 전국 각 시도의 출생률 데이터를 시각화합니다.")

# Folium 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)
folium.Choropleth(
    geo_data=merged_data_geojson,
    data=merged_data,
    columns=['행정구역', '출생률'],
    key_on='feature.properties.행정구역',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='출생률'
).add_to(m)

# Streamlit에 Folium 지도 표시
st_folium(m, width=800, height=600)
