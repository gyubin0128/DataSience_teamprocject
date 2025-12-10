import folium
import numpy as np

def create_fire_map(df, output_file='map.html'):
    """
    산불 발생 위치 및 피해 규모를 Folium 지도로 시각화하고 HTML 파일로 저장합니다.
    (주피터 노트북의 Cell 143 로직을 파이썬 함수로 변환)
    """
    if df is None:
        print("지도 시각화에 사용할 데이터가 없습니다.")
        return

    # 대한민국 중심 좌표
    korea_center = [36.5, 127.8]
    
    # Folium 지도 객체 생성
    m = folium.Map(location=korea_center, zoom_start=7)

    # 지도 시각화에 필요한 데이터만 필터링
    map_data = df.copy()
    map_data.dropna(subset=['위도', '경도', '피해면적_합계', '발생장소_시도'], inplace=True)
    
    # 피해 면적을 반지름에 사용할 수 있도록 스케일 조정 (로그 스케일 사용)
    # log1p를 사용하여 0에 가까운 값도 구분되도록 처리
    map_data['피해면적_adj'] = map_data['피해면적_합계'].apply(lambda x: max(x, 0.001))
    # 5000은 임의의 스케일링 팩터 (지도 크기에 따라 조정 필요)
    map_data['radius'] = np.log1p(map_data['피해면적_adj']) * 5000 

    # 산불 발생 지점을 CircleMarker로 지도에 추가
    for idx, row in map_data.iterrows():
        lat = row['위도']
        lon = row['경도']
        area_ha = row['피해면적_합계']
        radius = row['radius']
        location = row['발생장소_시도']
        
        # 팝업 내용
        popup_html = f"{location} / {area_ha:.2f} ha"

        # 피해 면적을 반지름으로 하는 Circle Marker 추가
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.5,
            popup=popup_html
        ).add_to(m)

    # 지도 저장 (map.html 파일 생성)
    m.save(output_file)
    print(f"지도 시각화 파일이 '{output_file}'로 저장되었습니다.")