import pandas as pd
import geokakao as gk
import numpy as np
import warnings

# SettingWithCopyWarning을 일시적으로 무시 (Pandas 경고 방지)
warnings.filterwarnings('ignore', category=pd.core.common.SettingWithCopyWarning)

def preprocess_data(df):
    """
    데이터프레임에 날짜/월, 통합 주소, 위경도 좌표, 진화 시간, 대형 산불 변수를 추가합니다.
    Datetime 변환 오류 및 결측치를 처리하여 데이터의 안정성을 높입니다.
    """
    if df is None:
        print("입력 데이터프레임이 None입니다.")
        return None

    initial_len = len(df)
    print(f"--- 데이터 전처리 시작 (초기 데이터: {initial_len}건) ---")

    # 1. 날짜/시간 컬럼 생성 및 진화 시간 계산
    print("... 시간 변수 및 진화 시간 계산 중...")
    
    # Datetime 변환 시, 원본 데이터의 잘못된 값(결측치, 문자열 등)을 NaT로 변환하여 Type Error 방지
    
    # 발생 시각 (YYYY-MM-DD HH)
    df['발생일시_DT'] = pd.to_datetime(
        df['발생일시_년'].astype(str) + '-' + 
        df['발생일시_월'].astype(str) + '-' + 
        df['발생일시_일'].astype(str) + ' ' + 
        df['발생일시_시간'].astype(str),
        errors='coerce' # 변환 불가 시 NaT 처리 (오류 방지 핵심)
    )
    
    # 진화 종료 시각 (YYYY-MM-DD HH)
    df['진화종료_DT'] = pd.to_datetime(
        df['진화종료_년'].astype(str) + '-' + 
        df['진화종료_월'].astype(str) + '-' + 
        df['진화종료_일'].astype(str) + ' ' + 
        df['진화종료_시간'].astype(str),
        errors='coerce' # 변환 불가 시 NaT 처리 (오류 방지 핵심)
    )

    # Sanity check: Datetime 변환 실패했거나 핵심 컬럼에 결측치가 있는 행 제거
    df.dropna(subset=['발생일시_DT', '진화종료_DT', '피해면적_합계'], inplace=True) 

    # 산불 진화 시간 (분 단위)
    # 두 Datetime 객체의 차이를 분 단위로 계산
    df['진화_시간_분'] = (df['진화종료_DT'] - df['발생일시_DT']).dt.total_seconds() / 60
    
    # 비정상적인 진화 시간 (음수 또는 과도하게 긴 시간) 제거 또는 처리
    # 음수는 데이터 오류이므로 제거
    df = df[df['진화_시간_분'] >= 0] 
    
    # 월의 시작 날짜로 변환하여 시계열 분석 기준 설정
    df['월'] = df['발생일시_DT'].dt.to_period('M').dt.to_timestamp()
    df['발생일'] = df['발생일시_DT'].dt.date # 기상 데이터 병합에 사용할 날짜 컬럼

    # 2. 주소 통합 및 Geocoding (좌표 변환)
    print("... 주소 통합 및 좌표 계산 중... (geokakao 사용)")
    df["주소"] = (
        df["발생장소_시도"].astype(str) + " " + 
        df["발생장소_시군구"].astype(str) + " " + 
        df["발생장소_읍면"].astype(str) + " " + 
        df["발생장소_동리"].astype(str)
    )
    
    # geokakao 사용 시, None 반환 가능성을 고려하여 처리
    df['coord'] = df['주소'].apply(gk.geocode)
    
    # x가 None인 경우를 대비하여 try-except 또는 조건문 처리
    df['경도'] = df['coord'].apply(lambda x: x[0] if isinstance(x, (tuple, list)) and len(x) == 2 else np.nan)
    df['위도'] = df['coord'].apply(lambda x: x[1] if isinstance(x, (tuple, list)) and len(x) == 2 else np.nan)
    df.drop(columns=['coord'], inplace=True, errors='ignore') # 'coord' 컬럼이 없으면 무시
    
    # 3. 대형 산불 변수 생성 (피해 면적 상위 10% 기준)
    if not df['피해면적_합계'].empty:
        threshold = df['피해면적_합계'].quantile(0.9)
        df['is_large_fire'] = (df['피해면적_합계'] >= threshold).astype(int)
        print(f"... 대형 산불 기준 피해 면적: {threshold:.2f} ha (상위 10%)")
    else:
        df['is_large_fire'] = 0
    
    # 4. 최종 결측치 처리 (좌표가 없는 행 제거)
    df.dropna(subset=['경도', '위도'], inplace=True)
    
    print(f"전처리 완료. 최종 {len(df)}건의 데이터 사용. ({initial_len - len(df)}건 제거)")
    
    # SettingWithCopyWarning 경고 필터 복원
    warnings.filterwarnings('default', category=pd.core.common.SettingWithCopyWarning)
    
    return df