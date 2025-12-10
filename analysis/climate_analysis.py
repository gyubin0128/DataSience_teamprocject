import pandas as pd
from scipy import stats

def analyze_suppression_time_by_humidity(df):
    """
    (가설 2 검증) 습도와 산불 진화 시간의 상관관계를 분석합니다.
    낮은 습도 그룹(평균 습도 하위 30%)과 높은 습도 그룹의 진화 시간을 T-test로 비교합니다.
    """
    if df is None or df['평균_습도'].isnull().all():
        print("습도 데이터가 없어 진화 시간 분석을 건너뜁니다.")
        return None

    # 습도 분위수 기반 그룹 나누기
    low_humidity_threshold = df['평균_습도'].quantile(0.3)
    
    # 30% 미만: 낮은 습도 그룹 (건조)
    low_humidity_group = df[df['평균_습도'] < low_humidity_threshold]['진화_시간_분'].dropna()
    
    # 70% 초과: 높은 습도 그룹 (습윤)
    high_humidity_threshold = df['평균_습도'].quantile(0.7)
    high_humidity_group = df[df['평균_습도'] > high_humidity_threshold]['진화_시간_분'].dropna()

    results = {}
    results['low_humidity'] = low_humidity_group.describe().to_dict()
    results['high_humidity'] = high_humidity_group.describe().to_dict()

    if len(low_humidity_group) > 1 and len(high_humidity_group) > 1:
        # 독립 표본 t-검정 수행 (진화 시간의 평균 차이 검증)
        t_stat, p_value = stats.ttest_ind(low_humidity_group, high_humidity_group, equal_var=False, nan_policy='omit')
        results['t_test'] = {'t_stat': t_stat, 'p_value': p_value}
    else:
        results['t_test'] = None
        
    print("습도별 진화 시간 분석 완료.")
    return results, low_humidity_group, high_humidity_group


def analyze_climate_factors_on_large_fire(df):
    """
    (가설 3 검증) 대형 산불 발생 시 기후 변수(습도, 풍속)의 평균을 비교합니다.
    """
    if df is None or df['is_large_fire'].isnull().all():
        print("대형 산불 또는 기후 데이터가 없어 분석을 건너뜜니다.")
        return None
        
    large_fire_df = df[df['is_large_fire'] == 1]
    normal_fire_df = df[df['is_large_fire'] == 0]

    comparison = pd.DataFrame({
        '대형 산불': large_fire_df[['평균_습도', '평균_풍속']].mean(),
        '일반 산불': normal_fire_df[['평균_습도', '평균_풍속']].mean()
    }).T
    
    print("대형 산불 기후 요인 평균 분석 완료.")
    return comparison