


import pandas as pd
import geopandas as gpd
import folium
from IPython.display import display, HTML

# 1. 출생률 데이터 로드 및 전처리
birth_rate_file = "C:/Users/chaet/Downloads/연령별_출산율_및_합계출산율_행정구역별__20241120143517.csv"
birth_rate_data = pd.read_csv(birth_rate_file, header=1, encoding='cp949')  # 인코딩 추가

# 열 이름 변경 및 필요 없는 행 제거
birth_rate_data.rename(columns={'행정구역별': '행정구역'}, inplace=True)

birth_rate_data.rename(columns={'합계출산율 (가임여성 1명당 명)': '출생률'}, inplace=True)
birth_rate_data = birth_rate_data[birth_rate_data['행정구역'] != '전국']  # '전국' 제거

# 사용할 열만 선택
birth_rate_data = birth_rate_data[['행정구역', '출생률']]

# 행정구역 이름 리스트
valid_regions = [
    '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
    '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도',
    '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'
]
birth_rate_data = birth_rate_data[birth_rate_data['행정구역'].isin(valid_regions)]

# 2. 지도 데이터 로드
geojson_file = "C:/Users/chaet/Downloads/data/gdf_korea_sido_2022.json"
geo_data = gpd.read_file(geojson_file)

# 지도 데이터에서 필요한 열만 추출 (지역명)
geo_data = geo_data[['geometry', 'CTP_KOR_NM']]  # 'CTP_KOR_NM'은 지역명 열
geo_data.rename(columns={'CTP_KOR_NM': '행정구역'}, inplace=True)

# 3. 출생률 데이터와 지도 데이터 병합
merged_data = geo_data.merge(birth_rate_data, how='inner', on='행정구역')

# 4. 지도 생성
# GeoDataFrame에서 GeoJSON 형식으로 변환
merged_data_geojson = merged_data.to_json()

# Choropleth 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

folium.Choropleth(
    geo_data=merged_data_geojson,  # GeoJSON 데이터로 전달
    data=merged_data,
    columns=['행정구역', '출생률'],  # 병합된 데이터의 열 이름
    key_on='feature.properties.행정구역',  # GeoJSON의 properties에서 행정구역 이름 매칭
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='출생률'
).add_to(m)

# 지도 출력
m.save('birth_rate_map.html')
display(HTML('birth_rate_map.html'))

# GeoDataFrame에서 GeoJSON 형식으로 변환
merged_data_geojson = merged_data.to_json()

# Choropleth 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

folium.Choropleth(
    geo_data=merged_data_geojson,  # GeoJSON 데이터로 전달
    data=merged_data,
    columns=['행정구역', '출생률'],  # 병합된 데이터의 열 이름
    key_on='feature.properties.행정구역',  # GeoJSON의 properties에서 행정구역 이름 매칭
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='출생률'
).add_to(m)

# 지도 출력
m.save('birth_rate_map.html')
display(HTML('birth_rate_map.html'))


m