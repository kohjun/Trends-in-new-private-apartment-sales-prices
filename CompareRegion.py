import tkinter as tk
from tkinter import ttk
import DataLoad
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CompareDisplayGraph:
    def __init__(self, root):
        self.rgd = DataLoad.RegionData('Trends-in-new-private-apartment-sales-prices-main\신규 민간아파트 분양가격.csv')

        # 현재 표시된 그래프를 저장하는 변수
        self.current_plot = None

        # 메인 프레임
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # 그래프를 표시할 프레임
        self.graph_frame = ttk.Frame(root)
        self.graph_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # 지역 목록
        self.regions = ['서울','인천','경기','부산','대구','광주','대전','울산','세종','강원','충북','충남','전북','전남','경북','경남','제주']

        # 현재 선택된 버튼을 저장하는 변수
        self.selected_button = None

        # 콤보박스 생성
        self.combobox = ttk.Combobox(self.main_frame, values=self.regions)
        self.combobox.set("서울")  # 초기 선택값 설정
        self.combobox.pack(side=tk.TOP, pady=5, anchor=tk.W)

        # 비교 콤보박스 생성
        self.compare_combobox = ttk.Combobox(self.main_frame, values=self.regions)
        self.compare_combobox.set("인천")  # 초기 선택값 설정
        self.compare_combobox.pack(side=tk.TOP, pady=5, anchor=tk.W)

        # 비교 버튼 생성
        compare_button = tk.Button(self.main_frame, text='Compare', command=self.compare_regions)
        compare_button.pack(side=tk.TOP, pady=5, anchor=tk.W)

        # 수치를 표시할 라벨
        self.result_label = tk.Label(self.main_frame, text='')
        self.result_label.pack(side=tk.TOP, pady=10, anchor=tk.W)


    def display_graph(self, selected_region, compare_region):
        # 기존 그래프가 있으면 제거
        if self.current_plot:
            self.current_plot.get_tk_widget().destroy()

        # 모든 지역의 데이터를 저장
        regionData = DataLoad.RegionData('Trends-in-new-private-apartment-sales-prices-main\신규 민간아파트 분양가격.csv')
        # 선택된 지역만의 데이터를 저장
        selected_region_data = regionData.get_data_by_region(selected_region)
        compare_region_data = regionData.get_data_by_region(compare_region)

        # 데이터프레임으로 변환
        df_selected = pd.DataFrame(selected_region_data)
        df_compare = pd.DataFrame(compare_region_data)

        # 분양가격(제곱미터) 컬럼을 숫자로 변환
        df_selected['분양가격(제곱미터)'] = pd.to_numeric(df_selected['분양가격(제곱미터)'], errors='coerce')
        df_compare['분양가격(제곱미터)'] = pd.to_numeric(df_compare['분양가격(제곱미터)'], errors='coerce')

        # 선택된 지역의 데이터에서 연도와 월별로 평균 분양가격 계산
        df_selected = df_selected.groupby(['연도', '월'])['분양가격(제곱미터)'].mean().reset_index()
        df_selected['연도월'] = df_selected['연도'].astype(str) + '-' + df_selected['월'].astype(str)

        # 비교 지역의 데이터에서 연도와 월별로 평균 분양가격 계산
        df_compare = df_compare.groupby(['연도', '월'])['분양가격(제곱미터)'].mean().reset_index()
        df_compare['연도월'] = df_compare['연도'].astype(str) + '-' + df_compare['월'].astype(str)

        # 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_selected['연도월'].astype(str), df_selected['분양가격(제곱미터)'], marker='o', markersize=3, linestyle='-', label="selected Region")
        ax.plot(df_compare['연도월'].astype(str), df_compare['분양가격(제곱미터)'], marker='o', markersize=3, linestyle='-', label="compare Region")
        ax.set_title('Comparison of Apartment Prices between Two Regions')
        ax.set_xlabel('Year-Month')
        ax.set_ylabel('Price per 1,000won')
        ax.legend()
        ax.grid(True)

        # 연도만 표시되도록 xticks 설정
        years = sorted(df_selected['연도'].unique())  # 데이터에 있는 모든 연도를 가져옴
        x_ticks_positions = range(0, len(df_selected['연도월']), len(years))
        ax.set_xticks(x_ticks_positions)  # x축에 표시할 눈금 위치를 연도로 설정
        ax.set_xticklabels(df_selected['연도월'].iloc[x_ticks_positions], ha='right')  # x축에 표시할 눈금 라벨을 연도로 설정

        # Tkinter 창에 Matplotlib 그림 삽입
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 현재 그래프 업데이트
        self.current_plot = canvas

        # 수치 표시
        avg_selected = df_selected['분양가격(제곱미터)'].mean()
        avg_compare = df_compare['분양가격(제곱미터)'].mean()
        result_text = f'Average Price for {selected_region}: {avg_selected:.2f} 천원\nAverage Price for {compare_region}: {avg_compare:.2f} 천원'
        self.result_label.config(text=result_text)

    def compare_regions(self):
        selected_region = self.combobox.get()
        compare_region = self.compare_combobox.get()
        self.display_graph(selected_region, compare_region)

