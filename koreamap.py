import os
import pandas as pd
import geopandas as gpd 
import folium
import json

import altair as alt
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import st_folium


# GeoJSON 파일 경로
geojson_file = "data/gg_map.json"

# GeoJSON 파일 읽기
geo_data = gpd.read_file(geojson_file)

# GeoDataFrame 정보 확인 (옵션)
print(geo_data.info())
print(geo_data.head())

geo_data.to_file("C:/Users/chaet/Downloads/gg_map.json",driver="GeoJSON")
with open("C:/Users/chaet/Downloads/gg_map.json",encoding='UTF-8') as f:
    data = json.load(f) 
    
print(json.dumps(data,indent=4,ensure_ascii=False)[0:400])


# 파일 경로 설정 (올바른 파일 이름과 경로를 입력)
file_path = "data/연령별_출산율_및_합계출산율_행정구역별__20241121121629.csv"

# 데이터 읽기 (첫 줄은 헤더로 제거)
data = pd.read_csv(file_path, header=1, encoding='cp949')

# 열 이름 변경
data.rename(columns={'행정구역별': '행정구역', '합계출산율 (가임여성 1명당 명)': '출생률'}, inplace=True)

# '행정구역'이 '전국'인 데이터 제거
data = data[data['행정구역'] != '전국']


# 드랍할 컬럼 리스트
columns_to_drop = [
    '모의 연령별출산율:15~19세 (해당연령 여자인구 1천명당 명)',
    '20~24세 (해당연령 여자인구 1천명당 명)',
    '25~29세 (해당연령 여자인구 1천명당 명)',
    '30~34세 (해당연령 여자인구 1천명당 명)',
    '35~39세 (해당연령 여자인구 1천명당 명)',
    '40~44세 (해당연령 여자인구 1천명당 명)',
    '45~49세 (해당연령 여자인구 1천명당 명)'
]

# 컬럼 드랍
data = data.drop(columns=columns_to_drop)

geo_data = geo_data.rename(columns={'NAME': '행정구역'})

# 공통 데이터 확인
common_regions = set(data['행정구역']).intersection(set(geo_data['행정구역']))

# data에만 있는 데이터
only_in_data = set(data['행정구역']).difference(set(geo_data['행정구역']))

# geo_data에만 있는 데이터
only_in_geo_data = set(geo_data['행정구역']).difference(set(data['행정구역']))

# 결과 출력
print(f"공통 데이터 개수: {len(common_regions)}")
print("공통 데이터:")
print(common_regions)

print(f"\ndata에만 있는 데이터 개수: {len(only_in_data)}")
print("data에만 있는 데이터:")
print(only_in_data)

print(f"\ngeo_data에만 있는 데이터 개수: {len(only_in_geo_data)}")
print("geo_data에만 있는 데이터:")
print(only_in_geo_data)

# '통합창원시'를 '창원'으로 변경
data['행정구역'] = data['행정구역'].replace('통합창원시', '창원시')


title='시군구 출생률'

korea_center = [36.505354, 127.704341]

# Streamlit 애플리케이션
st.title("전국 출생률 Choropleth 지도")
st.write("이 애플리케이션은 전국 각 시도의 출생률 데이터를 시각화합니다.")



gu_map=folium.Map(
    location=korea_center,
    zoom_start=7,
    tiles='cartodbpositron')


folium.Choropleth(
    geo_data=geo_data,
    data=data,
    columns=('행정구역', '출생률'),
    key_on='feature.properties.행정구역',  # GeoJSON의 '행정구역' 속성과 매칭
    fill_color='BuPu',  # 색상 팔레트
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='출생률'
).add_to(gu_map)


gu_map




