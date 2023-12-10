import tkinter as tk
from tkinter import ttk
import DataLoad
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DisplayGraph:
    def __init__(self, root):
        self.rgd = DataLoad.RegionData('신규 민간아파트 분양가격.csv')

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

        # 지역별 버튼 생성
        for region in self.regions:
            # 버튼 생성
            button = tk.Button(self.main_frame, text=region)
            button.pack(side=tk.TOP, pady=5, anchor=tk.W)  # pady는 수직 간격

            # 람다 함수에서 버튼을 사용하도록 수정
            button.config(command=lambda r=region, b=button: self.button_clicked(r, b))

    def display_graph(self, selected_region):
        # 기존 그래프가 있으면 제거
        if self.current_plot:
            self.current_plot.get_tk_widget().destroy()

        # 모든 지역의 데이터를 저장
        regionData = DataLoad.RegionData('신규 민간아파트 분양가격.csv')
        # 선택된 지역만의 데이터를 저장
        selected_region_data = regionData.get_data_by_region(selected_region)

        # 데이터프레임으로 변환
        df = pd.DataFrame(selected_region_data)

        # 분양가격(제곱미터) 컬럼을 숫자로 변환
        df['분양가격(제곱미터)'] = pd.to_numeric(df['분양가격(제곱미터)'], errors='coerce')



        # 선택된 지역의 데이터에서 연도와 월별로 평균 분양가격 계산
        df_selected = df.groupby(['연도', '월'])['분양가격(제곱미터)'].mean().reset_index()
        df_selected['연도월'] = df_selected['연도'].astype(str) + '-' + df_selected['월'].astype(str)

        # 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_selected['연도월'].astype(str), df_selected['분양가격(제곱미터)'], marker='o',markersize=3, linestyle='-', label='Selected Region')
        ax.set_title('Trends in new private apartment sales prices ')
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

    def button_clicked(self, region, button):
        # 모든 버튼의 색상 초기화
        for btn in self.main_frame.winfo_children():
            btn.config(bg='SystemButtonFace')

        # 현재 버튼의 색상 변경
        button.config(bg='lightblue')
        self.selected_button = button

        # 버튼 클릭 시 display_graph 함수 호출
        self.display_graph(region)