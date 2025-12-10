import pandas as pd

def calculate_monthly_trends(df):
    """
    월별 발생 건수, 총 피해 면적, 평균 피해 면적을 집계하여 반환합니다.
    (주피터 노트북의 월별 집계 로직 반영)
    """
    if df is None:
        return None
    
    # 월별 발생 건수 + 총 피해면적 + 평균 피해면적 집계
    monthly = df.groupby('월').agg(
        발생건수 = ('발생일', 'count'),
        총피해면적 = ('피해면적_합계', 'sum'),
        평균피해면적 = ('피해면적_합계', 'mean')
    ).reset_index()

    print("월별 트렌드 분석 완료.")
    return monthly