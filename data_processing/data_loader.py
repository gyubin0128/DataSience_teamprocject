import pandas as pd
import os

def load_data(file_path='data/산림청_산불통계데이터_20250911.csv'):
    """
    산불 데이터를 CSV 파일에서 불러와 판다스 DataFrame으로 반환합니다.
    여러 인코딩을 시도하여 한글 깨짐을 방지합니다.
    """
    # 시도할 인코딩 리스트
    encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"   데이터 로드 성공! (인코딩: {encoding})")
            print(f"   총 {len(df)}건의 데이터")
            print(f"   컬럼: {list(df.columns)[:5]}...")  # 처음 5개 컬럼만 출력
            return df
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        except Exception as e:
            print(f"    {encoding} 인코딩 실패: {e}")
            continue
    
    # 모든 인코딩 실패시
    print(f"   오류: 파일을 읽을 수 없습니다.")
    print(f"   경로: {file_path}")
    print(f"   시도한 인코딩: {encodings}")
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"   파일이 존재하지 않습니다!")
        # data 폴더의 파일 목록 출력
        data_dir = os.path.dirname(file_path)
        if os.path.exists(data_dir):
            print(f"\n   '{data_dir}' 폴더의 파일 목록:")
            for f in os.listdir(data_dir):
                if f.endswith('.csv'):
                    print(f"      - {f}")
    
    return None