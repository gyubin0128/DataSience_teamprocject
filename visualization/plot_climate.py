import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False 

def plot_suppression_time_boxplot(low_group, high_group):
    """
    (가설 2 검증 시각화) 낮은 습도와 높은 습도 그룹의 산불 진화 시간 분포를 Box Plot으로 비교합니다.
    """
    if low_group.empty or high_group.empty:
        print("진화 시간 분포를 비교할 데이터가 충분하지 않습니다.")
        return

    data_to_plot = pd.DataFrame({
        '습도 그룹': ['낮음 (건조)'] * len(low_group) + ['높음 (습윤)'] * len(high_group),
        '진화_시간_분': pd.concat([low_group, high_group])
    })

    plt.figure(figsize=(8, 6))
    sns.boxplot(x='습도 그룹', y='진화_시간_분', data=data_to_plot, palette=['#FFC300', '#3498DB'])
    plt.title('습도 그룹별 산불 진화 시간 비교 (가설 2 검증)')
    plt.ylabel('진화 시간 (분)')
    plt.xlabel('')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()

def plot_large_fire_climate_comparison(comparison_df):
    """
    (가설 3 검증 시각화) 대형 산불과 일반 산불의 주요 기후 변수(습도, 풍속) 평균을 막대 그래프로 비교합니다.
    """
    if comparison_df is None:
        print("대형 산불 기후 비교 데이터가 없습니다.")
        return

    comparison_df.T.plot(kind='bar', figsize=(8, 6), rot=0, 
                         color={'평균_습도': '#3498DB', '평균_풍속': '#E74C3C'})
    plt.title('대형 산불 vs. 일반 산불 시점의 평균 기후 조건')
    plt.ylabel('값')
    plt.xticks(fontsize=12)
    plt.legend(title='기후 변수')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.show()