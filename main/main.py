import os
import pandas as pd

# 데이터 처리 모듈 임포트
from data_processing.data_loader import load_data
from data_processing.feature_engineer import preprocess_data
# 신규 모듈 임포트
from data_processing.mock_climate_data_loader import create_mock_climate_data, merge_climate_data 

# 분석 모듈 임포트
from analysis.monthly_analysis import calculate_monthly_trends
from analysis.cause_analysis import calculate_cause_proportions, calculate_human_cause_comparison
# 신규 모듈 임포트
from analysis.climate_analysis import analyze_suppression_time_by_humidity, analyze_climate_factors_on_large_fire

# 시각화 모듈 임포트
from visualization.plot_trends import plot_monthly_trends
from visualization.plot_causes import plot_cause_proportions, plot_human_cause_comparison
from visualization.visualize_map import create_fire_map
# 신규 모듈 임포트
from visualization.plot_climate import plot_suppression_time_boxplot, plot_large_fire_climate_comparison

def main():
    """
    산불 데이터 분석 및 시각화 프로젝트의 전체 실행 파이프라인.
    """
    print("--- 산불 데이터 분석 프로젝트 시작 ---")
    
    # 1. 데이터 로드 및 전처리 (진화 시간 및 대형 산불 변수 생성)
    raw_df = load_data()
    processed_df = preprocess_data(raw_df)
    if processed_df is None:
        return
    
    # DOCX 핵심 단계 1: 기상 데이터 결합
    # 실제 기상 데이터가 없으므로 Mock 데이터를 생성하여 병합합니다.
    climate_df = create_mock_climate_data(processed_df)
    final_df = merge_climate_data(processed_df, climate_df)
    
    # 2. 분석 수행
    monthly_trends = calculate_monthly_trends(final_df)
    cause_proportions = calculate_cause_proportions(final_df)
    
    # 2-1. 원인별 비율 비교 (요청 구현 항목)
    human_cause_comp = calculate_human_cause_comparison(final_df)
    
    # 2-2. 기후 요인 분석 (가설 2, 3 검증)
    # 가설 2: 습도별 진화 시간 분석
    t_test_results, low_hum_group, high_hum_group = analyze_suppression_time_by_humidity(final_df)
    
    # 가설 3: 대형 산불 기후 요인 평균 비교
    large_fire_climate_comp = analyze_climate_factors_on_large_fire(final_df)

    # 3. 시각화 수행
    print("\n--- 분석 결과 시각화 ---")

    # 3-1. 기존 시각화
    plot_monthly_trends(monthly_trends, scale='standard')
    plot_monthly_trends(monthly_trends, scale='log')
    plot_cause_proportions(cause_proportions, top_n=10)
    
    # 3-2. 원인별 비율 비교 시각화 (요청 구현 항목)
    plot_human_cause_comparison(human_cause_comp)

    # 3-3. 기후 요인 분석 시각화 (DOCX 가설 검증)
    plot_suppression_time_boxplot(low_hum_group, high_hum_group)
    plot_large_fire_climate_comparison(large_fire_climate_comp)
    
    # 3-4. 지도 시각화
    map_output_file = os.path.join(os.getcwd(), 'map.html')
    create_fire_map(final_df, output_file=map_output_file)
    
    print("\n--- 프로젝트 실행 완료 ---")

if __name__ == "__main__":
    main()