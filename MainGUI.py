import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from DataLoad import RegionData
from tkinter import ttk
import pandas as pd
import CompareRegion
import RegionButton
import Calculate
from mp3 import ContinuousMusicPlayer


# 지역 목록
regions = ['서울','인천','경기','부산','대구','광주','대전','울산','세종','강원','충북','충남','전북','전남','경북','경남','제주']

class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('아파트 서비스 플랫폼 토아')
        self.geometry("1024x768+100+100")
        self.resizable(False, False)
        self.configure(bg='white')

        # 초기 화면 설정
        self.home_screen()
        music_file_path = "MP_오늘의 먹방.mp3"  # 실제 MP3 파일 경로로 변경
        app = ContinuousMusicPlayer(self, music_file_path)

    def home_screen(self):
        # 제목
        label_1 = tk.Label(self, text="아파트 서비스 플랫폼 토아", width=20, height=5, fg="grey", bg="white",font=("Helvetica", 16, "bold italic"))
        label_1.place(x=10,y=10)
        label_1.pack()
        #RegionButton.DisplayGraph(self)

        # 홈 버튼 (오른쪽 상단)
        home_button = tk.Button(self, text="Home", command=self.show_home)
        home_button.place(relx=0.9, rely=0.1, anchor="center")

        # 지역 가격추이 이벤트
        region_button = tk.Button(self, text="지역 가격 추이", command=self.show_region_event)
        region_button.place(relx=0.1, rely=0.1, anchor="center")

        # 지역 가격예측 이벤트
        predict_button = tk.Button(self, text="지역 가격 예측", command=self.show_predict_event)
        predict_button.place(relx=0.2, rely=0.1, anchor="center")

        # 지역 가격예측 이벤트
        predict_button = tk.Button(self, text="지역 가격 비교", command=self.show_compare_event)
        predict_button.place(relx=0.3, rely=0.1, anchor="center")


    def show_home(self):
        # 홈 버튼 눌렀을 때의 동작 (다른 기능 비활성화)
        for widget in self.winfo_children():
            widget.destroy()
        self.home_screen()

    def show_region_event(self):
        self.show_home()
        RegionButton.DisplayGraph(self)

    def show_predict_event(self):
        self.show_home()
        Calculate.ApartmentPricePredictor(self)
    def show_compare_event(self):
        self.show_home()
        CompareRegion.CompareDisplayGraph(self)


if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
