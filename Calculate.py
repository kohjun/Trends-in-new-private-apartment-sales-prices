import tkinter as tk
from tkinter import ttk
import MachineLearning

class ApartmentPricePredictor:
    def __init__(self, master):
        self.master = master


        # 결과를 표시할 라벨 생성
        self.result_label = tk.Label(master, text="",font=("Helvetica", 15), width=50,height=15,wraplength=600)
        self.result_label.pack(side="top", pady=(0,20))  # pack 사용 

        # 표 생성
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("전용면적(m^2)","전용면적(평)","아파트 평형","가격")
        

        # 각 열(column) 설정
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("전용면적(m^2)", anchor=tk.W, width=100)
        self.tree.column("전용면적(평)", anchor=tk.CENTER, width=100)
        self.tree.column("아파트 평형", anchor=tk.W, width=100)
        self.tree.column("가격", anchor=tk.W, width=100)

        # 열 제목 설정
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("전용면적(m^2)", text="전용면적(m^2)", anchor=tk.W)
        self.tree.heading("전용면적(평)", text="전용면적(평)", anchor=tk.CENTER)
        self.tree.heading("아파트 평형", text="아파트 평형", anchor=tk.W)
        self.tree.heading("가격", text="가격(원)", anchor=tk.W)

        # 표 출력
        self.tree.pack(side="bottom",expand=tk.YES, fill=tk.BOTH)
  

        # 지역 라벨 및 선택 창
        self.region_label, self.region_combobox = self.create_label_and_combobox("지역", 1, ['서울','인천','경기','부산','대구','광주','대전','울산','세종','강원','충북','충남','전북','전남','경북','경남','제주'])

        # 예측 연도 라벨 및 선택 창
        self.year_label, self.year_combobox = self.create_label_and_combobox("예측 연도", 2, list(range(2023, 2040)))

        # 통화량 증가율 라벨 및 입력 창
        self.increase_label, self.increase_entry = self.create_label_and_entry("통화량 증가율", 3)

        # 경제 성장률 라벨 및 입력 창
        self.growth_label, self.growth_entry = self.create_label_and_entry("경제 성장률", 4)

        # 버튼 생성
        button = tk.Button(master, text="예측하기", command=self.on_button_click)
        button.pack(side="left", padx=5, pady=5)  # pack 사용


    def add_data(self, x, y, z,r):
        self.tree.insert("", tk.END, values=(x,y,z,r))   

    def create_label_and_combobox(self, label_text, row, values):
        # 라벨 생성
        label = tk.Label(self.master, text=label_text)
        label.pack(side="left", padx=5, pady=5)  # pack 사용

        # 선택 창 생성
        combobox = ttk.Combobox(self.master, values=values, state="readonly")
        combobox.pack(side="left", padx=5, pady=5)  # pack 사용
        return label, combobox

    def create_label_and_entry(self, label_text, row):
        # 라벨 생성
        label = tk.Label(self.master, text=label_text)
        label.pack(side="left", padx=5, pady=5)  # pack 사용

        # 입력 창 생성
        entry = tk.Entry(self.master)
        entry.pack(side="left", padx=5, pady=5)  # pack 사용

        return label, entry

    def calculate_result(self, parameter):
        # 간단한 계산 예시. 실제로는 여러 파라미터를 활용하여 원하는 연산을 구현하세요.
        result = parameter
        return result

    def on_button_click(self):
       # 사용자가 입력한 값을 가져오기
        ip1 = self.region_combobox.get()
        ip2 = int(self.year_combobox.get())
        ip3 = float(self.increase_entry.get())
        ip4 = float(self.growth_entry.get())

        try:
            # 입력값을 실수로 변환하여 함수에 전달하고 결과를 출력
            input_machine_learning = MachineLearning.Input_MachineLearning(ip1, ip2, ip3, ip4)
            predicted_price = input_machine_learning.get_prediction()
            r2_score_result = input_machine_learning.get_evaluation()
            self.result_label.config(text=f"{ip2}년 {ip1} 지역 아파트 분양가격 예측: {predicted_price}천원/제곱미터, 결정계수: {round(r2_score_result,2)}")
            
            # 데이터 추가
            self.add_data("19", "6평", "8평형대",predicted_price*19000)
            self.add_data("21", "6평", "9평형대",predicted_price*21000)
            self.add_data("24", "7평", "10평형대",predicted_price*24000)
            self.add_data("29", "9평", "12평형대",predicted_price*29000)
            self.add_data("34", "10평", "14평형대",predicted_price*34000)
            self.add_data("39", "12평", "16평형대",predicted_price*39000)
            self.add_data("44", "13평", "18평형대",predicted_price*44000)
            self.add_data("69", "21평", "28평형대",predicted_price*69000)
            self.add_data("74", "22평", "30평형대",predicted_price*74000)    
            self.add_data("84", "25평", "34평형대",predicted_price*84000)
            self.add_data("101", "31평", "41평형대",predicted_price*101000)
            self.add_data("119", "36평", "49평형대",predicted_price*119000)
            self.add_data("140", "42평", "61평형대",predicted_price*140000)

            
            # 표 출력
            self.tree.pack(side="bottom",expand=tk.YES, fill=tk.BOTH)
        except ValueError:
            # 입력값이 실수로 변환되지 않으면 오류 메시지 출력
            self.result_label.config(text="입력값은 실수여야 합니다.")

