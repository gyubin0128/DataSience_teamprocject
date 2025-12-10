import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Matplotlib 한글 설정 (주피터 노트북에서 사용된 설정으로 가정)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

def plot_monthly_trends(monthly_df, scale='standard'):
    # ... (기존 코드 유지)
    pass

def plot_cause_proportions(cause_df, top_n=10):
    # ... (기존 코드 유지)
    pass

def plot_human_cause_comparison(comparison_df):
    """
    전국과 다발 지역의 산불 발생 인적 요인 비율을 누적 막대 그래프로 비교 시각화합니다.
    """
    if comparison_df is None:
        print("비교 시각화할 데이터가 없습니다.")
        return

    labels = comparison_df['지역구분']
    human_ratio = comparison_df['인적 요인 비율 (%)']
    other_ratio = comparison_df['자연/기타 비율 (%)']

    width = 0.5
    fig, ax = plt.subplots(figsize=(8, 6))

    # 자연/기타 비율 (바닥)
    ax.bar(labels, other_ratio, width, label='자연/기타 요인', color='#3498DB')
    # 인적 요인 비율 (누적)
    bars = ax.bar(labels, human_ratio, width, bottom=other_ratio, label='인적 요인', color='#E74C3C')

    # 비율 텍스트 표시
    for bar, ratio in zip(bars, human_ratio):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., 
                bar.get_y() + height - 5,
                f'{ratio:.1f}%',
                ha='center', va='bottom', color='white', fontweight='bold')

    ax.set_ylabel('발생 비율 (%)')
    ax.set_title('전국 대비 산불 다발 지역의 인적 요인 비율 비교 (가설 1 관련)')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()