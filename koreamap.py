import os
import pandas as pd
import geopandas as gpd 
import folium
import streamlit as st
from streamlit_folium import st_folium

# GeoJSON 파일 경로
geojson_file = "data/gg_map.json"

# GeoJSON 파일 읽기
geo = gpd.read_file(geojson_file)

# GeoDataFrame 열 이름 변경
geo = geo.rename(columns={'NAME': '행정구역'})
geo.to_file("data/updated_gg_map.json", driver="GeoJSON")  # 저장 위치 확인

# CSV 파일 경로
file_path = "data/연령별_출산율_및_합계출산율_행정구역별__20241121121629.csv"

# 데이터 읽기
birth = pd.read_csv(file_path, header=1, encoding='cp949')

# 열 이름 변경
birth.rename(columns={'행정구역별': '행정구역', '합계출산율 (가임여성 1명당 명)': '출생률'}, inplace=True)

# 데이터 정제
birth = birth[birth['행정구역'] != '전국']
birth['행정구역'] = birth['행정구역'].str.strip()
geo['행정구역'] = geo['행정구역'].str.strip()

# Folium 지도 생성
korea_center = [36.505354, 127.704341]  # 대한민국 중심 좌표
gu_map = folium.Map(location=korea_center, zoom_start=7, tiles='cartodbpositron')

# Choropleth 지도 추가
folium.Choropleth(
    geo_data="data/updated_gg_map.json",
    data=birth,
    columns=['행정구역', '출생률'],
    key_on='feature.properties.행정구역',
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='출생률'
).add_to(gu_map)

# Streamlit에서 Folium 지도 렌더링
st.title("전국 출생률 Choropleth 지도")
st.write("이 애플리케이션은 전국 각 시도의 출생률 데이터를 시각화합니다.")
st_folium(gu_map, width=800, height=600)



