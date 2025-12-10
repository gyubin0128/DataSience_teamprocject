import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

# Matplotlib 한글 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

def plot_monthly_trends(monthly_df, scale='standard'):
    """
    월별 산불 발생 건수와 피해 면적을 이중 축 그래프로 시각화합니다.
    scale: 'standard' (일반) 또는 'log' (로그 스케일)
    (주피터 노트북의 Cell 145, 146 로직 반영)
    """
    if monthly_df is None:
        print("시각화할 월별 데이터가 없습니다.")
        return

    fig, ax1 = plt.subplots(figsize=(15, 6))

    # --- 축 1: 발생 건수 (왼쪽) ---
    color_count = 'tab:blue'
    ax1.set_xlabel('월별')
    ax1.set_ylabel('발생 건수', color=color_count)
    line1 = ax1.plot(monthly_df['월'], monthly_df['발생건수'], color=color_count, label='발생 건수', marker='o')
    ax1.tick_params(axis='y', labelcolor=color_count)

    title_text = '월별 산불 발생 건수 / 총 피해면적 / 평균 피해면적 비교'
    if scale == 'log':
        ax1.set_yscale('log')
        title_text = '월별 산불 트렌드 (로그 스케일) 비교'
    ax1.set_title(title_text)

    # --- 축 2: 총 피해면적 및 평균 피해면적 (오른쪽) ---
    ax2 = ax1.twinx()  
    
    # 총 피해면적
    color_area = 'tab:red'
    line2 = ax2.plot(monthly_df['월'], monthly_df['총피해면적'], color=color_area, linestyle='--', label='총 피해면적 (ha)', marker='s')
    
    # 평균 피해면적
    color_mean = 'tab:green'
    line3 = ax2.plot(monthly_df['월'], monthly_df['평균피해면적'], color=color_mean, linestyle=':', label='평균 피해면적 (ha)', marker='d')
    
    ax2.set_ylabel('피해면적 (ha)', color=color_area)
    ax2.tick_params(axis='y', labelcolor=color_area)
    
    # 로그 스케일일 경우 축 2도 로그 스케일 적용
    if scale == 'log':
        ax2.set_yscale('log')
        
    # 범례 합치기
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    # X축 포맷 설정
    # .dt.to_timestamp()를 사용했으므로 자동으로 시간축 포맷팅됨. 여기서는 간소화
    ax1.xaxis.set_major_formatter(ticker.Formatter.null_formatter) 
    
    plt.grid(True)
    plt.tight_layout()
    plt.show()