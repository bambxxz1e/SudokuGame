import tkinter as tk
from SudokuMain import SudokuGame

def start():
    root.destroy()  # 기존 시작 창 종료
    game = SudokuGame()
    game.start_game()  # 게임 시작

root = tk.Tk()
root.title("스도쿠 게임")
root.geometry("250x300")

start_btn = tk.Button(root, text="시작하기", command=start, bg="lightblue")
start_btn.place(x=85, y=90, width=80, height=50)

root.mainloop()