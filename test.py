import tkinter as tk

def change_label_text():
    label.config(text="수정된 텍스트")

root = tk.Tk()

# 초기 라벨 생성
label = tk.Label(root, text="원본 텍스트")
label.pack(pady=10)

# 버튼 생성
button = tk.Button(root, text="텍스트 수정", command=change_label_text)
button.pack()

root.mainloop()
