import tkinter as tk
from pygame import mixer

class ContinuousMusicPlayer:
    def __init__(self, master, music_file):
        self.master = master
        self.music_file = music_file

        # 초기화
        mixer.init()
        mixer.music.load(self.music_file)
        mixer.music.play(loops=-1)  # -1은 반복 재생을 의미


        # 종료 이벤트 처리
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        # 종료 버튼을 누르면 호출되는 함수
        mixer.music.stop()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    music_file_path = "Trends-in-new-private-apartment-sales-prices-main\MP_오늘의 먹방.mp3"  # 실제 MP3 파일 경로로 변경
    app = ContinuousMusicPlayer(root, music_file_path)
    root.mainloop()
