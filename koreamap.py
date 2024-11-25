import os
import pandas as pd
import geopandas as gpd 
import folium
import json
import streamlit as st
from streamlit_folium import st_folium  # st_folium을 사용하여 Folium 지도 렌더링

# GeoJSON 파일 경로
geojson_file = "data/gg_map.json"

# GeoJSON 파일 읽기
geo = gpd.read_file(geojson_file)

# GeoDataFrame 열 이름 변경
geo = geo.rename(columns={'NAME': '행정구역'})

# CSV 파일 경로
file_path = "data/연령별_출산율_및_합계출산율_행정구역별__20241121121629.csv"

# 데이터 읽기
birth = pd.read_csv(file_path, header=1, encoding='cp949')

# 열 이름 변경
birth.rename(columns={'행정구역별': '행정구역', '합계출산율 (가임여성 1명당 명)': '출생률'}, inplace=True)

# '전국' 데이터 제외 및 필요 없는 열 제거
birth = birth[birth['행정구역'] != '전국']
columns_to_drop = [
    '모의 연령별출산율:15~19세 (해당연령 여자인구 1천명당 명)',
    '20~24세 (해당연령 여자인구 1천명당 명)',
    '25~29세 (해당연령 여자인구 1천명당 명)',
    '30~34세 (해당연령 여자인구 1천명당 명)',
    '35~39세 (해당연령 여자인구 1천명당 명)',
    '40~44세 (해당연령 여자인구 1천명당 명)',
    '45~49세 (해당연령 여자인구 1천명당 명)'
]
birth = birth.drop(columns=columns_to_drop)

# '통합창원시'를 '창원시'로 변경
birth['행정구역'] = birth['행정구역'].replace('통합창원시', '창원시')


# 공통 데이터 확인
common_regions = set(birth['행정구역']).intersection(set(geo['행정구역']))
if not common_regions:
    print("공통된 '행정구역' 데이터가 없습니다. 데이터셋을 확인하세요.")
else:
    print(f"공통된 '행정구역' 개수: {len(common_regions)}")

# Folium 지도 생성
korea_center = [36.505354, 127.704341]  # 대한민국 중심 좌표
gu_map = folium.Map(location=korea_center, zoom_start=7, tiles='cartodbpositron')

# Choropleth 지도 추가
folium.Choropleth(
    geo_data=geo,
    data=birth,
    columns=['행정구역', '출생률'],
    key_on='feature.properties.NAME',  # GeoJSON의 '행정구역' 속성과 매칭
    fill_color='BuPu',  # 색상 팔레트
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='출생률'
).add_to(gu_map)

# Streamlit에서 Folium 지도 렌더링
st.title("전국 출생률 Choropleth 지도")
st.write("이 애플리케이션은 전국 각 시도의 출생률 데이터를 시각화합니다.")

st_folium(gu_map, width=800, height=600, returned_objects=[])




