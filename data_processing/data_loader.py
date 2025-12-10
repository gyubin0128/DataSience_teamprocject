import pandas as pd

def load_data(file_path='산림청_산불통계데이터_20250911.csv'):
    """
    산불 통계 데이터를 CSV 파일에서 로드하여 데이터프레임을 반환합니다.
    """
    try:
        # 원본 파일명 및 인코딩 (cp949) 사용
        df = pd.read_csv(file_path, encoding='cp949')
        print(f"데이터 로드 성공: {len(df)}건")
        return df
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다. 경로를 확인해주세요: {file_path}")
        return None
    except Exception as e:
        print(f"오류 발생: {e}")
        return None