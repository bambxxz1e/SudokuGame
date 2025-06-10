import tkinter as tk
from tkinter import *

class Trans:
    def __init__(self, root):
        self.root = root
        self.root.title("투명도 조절기")
        self.root.geometry("300x130")

        self.slide_label = tk.Label(self.root, text="투명도: 1.0")
        self.slide_label.pack(pady=5)

        self.slide_bar = tk.Scale(self.root, from_=0.1, to=1.0, resolution=0.01,
                                  orient=HORIZONTAL, command=self.slide)
        self.slide_bar.set(1.0)
        self.slide_bar.pack(pady=5)

        self.save_btn = Button(self.root, text="적용", command=self.save_transparency)
        self.save_btn.pack(side="bottom", pady=5)

    def slide(self, val):
        # 슬라이더 움직일 때 투명도 값만 보여줌
        self.slide_label.config(text=f"투명도: {round(float(val), 2)}")

    def save_transparency(self):
        alpha = self.slide_bar.get()
        self.root.attributes('-alpha', alpha)
        self.slide_label.config(text=f"적용됨: {round(alpha, 2)}")

if __name__ == "__main__":
    app = tk.Tk()
    trans = Trans(app)
    app.mainloop()


