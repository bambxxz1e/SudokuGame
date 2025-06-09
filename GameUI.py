import tkinter as tk
from tkinter import messagebox

class GameUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("스도쿠 게임")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.display_grid()

    def display_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, justify="center", font=("Arial", 16))
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.bind("<FocusOut>", lambda e, r=i, c=j: self.on_cell_click(r, c))
                self.cells[i][j] = entry

        tk.Button(self.root, text="게임 상태 확인", command=self.on_double_click).grid(row=10, column=0, columnspan=9)

    def on_cell_click(self, row, col):
        try:
            value = int(self.cells[row][col].get())
            self.game.board.set_cell(row, col, value)
        except ValueError:
            self.game.board.clear_cell(row, col)

    def on_double_click(self):
        self.game.check_game_status()

    def show_message(self, msg):
        messagebox.showinfo("알림", msg)

    def show_restart_button(self):
        tk.Button(self.root, text="다시 시작", command=self.game.start_game).grid(row=11, column=0, columnspan=9)

    def run(self):
        self.root.mainloop()
