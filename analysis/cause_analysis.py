import pandas as pd

HUMAN_CAUSES = ['입산자 실화', '논/밭두렁 소각', '쓰레기 소각', '담뱃불', '어린이 불장난', '기타'] 

def calculate_monthly_trends(df):
    # ... (기존 코드 유지)
    pass

def calculate_cause_proportions(df, cause_column='발생원인_세부원인'):
    # ... (기존 코드 유지)
    pass

def calculate_human_cause_comparison(df, top_n_area=10):
    """
    전국 대비 산불 다발 지역의 인적 요인 비율을 계산합니다.
    (다발 지역은 발생 건수 기준 상위 N개 시도로 임의 지정)
    """
    if df is None:
        return None

    # 1. 다발 지역 선정 (발생 건수 기준 상위 N개 시도)
    top_areas = df.groupby('발생장소_시도').size().nlargest(top_n_area).index
    df_hotspot = df[df['발생장소_시도'].isin(top_areas)]
    
    analysis_results = {}

    # 2. 전국 및 다발 지역의 인적 요인 비율 계산 함수
    def get_human_ratio(data, name):
        total_count = len(data)
        human_count = data[data['발생원인_세부원인'].isin(HUMAN_CAUSES)].shape[0]
        
        analysis_results[name] = {
            '인적 요인 비율 (%)': (human_count / total_count) * 100,
            '자연/기타 비율 (%)': 100 - (human_count / total_count) * 100
        }

    # 3. 전국 비율 계산
    get_human_ratio(df, '전국')
    
    # 4. 다발 지역 비율 계산
    get_human_ratio(df_hotspot, f'다발 지역 (Top {top_n_area})')

    # 시각화를 위한 DataFrame 변환
    comparison_df = pd.DataFrame(analysis_results).T.reset_index(names='지역구분')
    print("전국 vs. 다발 지역 인적 요인 비율 비교 분석 완료.")
    return comparison_df