import pandas as pd
import numpy as np
import random

def create_mock_climate_data(fire_df):
    """
    산불 데이터의 발생일 및 지역 정보를 기반으로 가상의 기상 데이터를 생성합니다.
    (실제 분석 시에는 ASOS/AWS 데이터 로드 및 전처리 코드로 대체되어야 함)
    """
    print("... 가상 기상 데이터 생성 중...")
    
    # 산불 데이터의 고유한 발생일-지역 조합 추출
    unique_keys = fire_df[['발생일', '발생장소_시도']].drop_duplicates()
    
    # 각 조합에 대해 가상 기상 변수 생성
    mock_data = unique_keys.copy()
    
    # 습도 (상대습도) - 산불 발생 시 낮은 경향 (평균 40~60)
    mock_data['평균_습도'] = np.round(np.random.normal(loc=50, scale=15, size=len(mock_data)), 1)
    mock_data['평균_습도'] = mock_data['평균_습도'].clip(0, 100) # 0%~100% 사이로 제한

    # 풍속 (평균 풍속 m/s) - 산불 발생 시 높은 경향 (평균 2~5)
    mock_data['평균_풍속'] = np.round(np.random.normal(loc=3, scale=2, size=len(mock_data)), 1)
    mock_data['평균_풍속'] = mock_data['평균_풍속'].clip(0.1, 10) 

    # 강수량 (mm) - 산불 발생 시 0에 가까움
    mock_data['일_강수량'] = np.round(np.random.lognormal(mean=0.01, sigma=0.5, size=len(mock_data)) / 100, 2)
    mock_data['일_강수량'] = mock_data['일_강수량'].clip(0, 5)

    print("가상 기상 데이터 생성 완료.")
    return mock_data

def merge_climate_data(fire_df, climate_df):
    """
    산불 통계 데이터와 기상 데이터를 발생일 및 시도 기준으로 결합합니다.
    (DOCX의 '핵심 변수 결합' 로직 구현)
    """
    if fire_df is None or climate_df is None:
        return fire_df

    print("... 산불 데이터와 기상 데이터 병합 중...")
    
    # 발생일과 시도를 기준으로 병합 (Left Merge)
    merged_df = pd.merge(
        fire_df, 
        climate_df, 
        on=['발생일', '발생장소_시도'], 
        how='left'
    )
    
    print("데이터 병합 완료.")
    return merged_df