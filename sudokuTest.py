import random
import tkinter as tk
from tkinter import messagebox

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[box_row + i][box_col + j] == num:
                    return False

        return True

    def fill_grid(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(i, j, num):
                            self.grid[i][j] = num
                            if self.fill_grid():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True

    def count_solutions(self, grid):
        count = [0]

        def solve():
            if count[0] > 1:
                return
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        for num in range(1, 10):
                            if self.is_valid_cell(grid, i, j, num):
                                grid[i][j] = num
                                solve()
                                grid[i][j] = 0
                        return
            count[0] += 1

        solve()
        return count[0]

    def is_valid_cell(self, grid, row, col, num):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if grid[box_row + i][box_col + j] == num:
                    return False
        return True

    def generate_puzzle(self):
        self.fill_grid()
        puzzle = [row[:] for row in self.grid]

        attempts = 30
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while puzzle[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            copy = [r[:] for r in puzzle]
            if self.count_solutions(copy) != 1:
                puzzle[row][col] = backup
                attempts -= 1
        return puzzle

class SudokuUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("스도쿠 게임")
        self.generator = SudokuGenerator()
        self.puzzle = self.generator.generate_puzzle()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.fixed_cells = {(i, j) for i in range(9) for j in range(9) if self.puzzle[i][j] != 0}
        self.create_widgets()

    def create_widgets(self):
        colors = ['#ffffff', '#e6f7ff']
        for i in range(9):
            for j in range(9):
                color_index = ((i // 3) + (j // 3)) % 2
                entry = tk.Entry(self.root, width=2, font=("Arial", 16), justify="center",
                                 bg=colors[color_index])
                if (i, j) in self.fixed_cells:
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(state="readonly", disabledforeground="black")
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

        reset_btn = tk.Button(self.root, text="초기화", command=self.reset_inputs)
        reset_btn.grid(row=9, column=0, columnspan=3, pady=10)

        check_btn = tk.Button(self.root, text="정답 확인", command=self.check_solution)
        check_btn.grid(row=9, column=3, columnspan=3, pady=10)

    def reset_inputs(self):
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.fixed_cells:
                    self.entries[i][j].delete(0, tk.END)

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.fixed_cells:
                    val = self.entries[i][j].get()
                    if not val.isdigit() or not (1 <= int(val) <= 9):
                        messagebox.showerror("오류", "모든 칸을 1~9 사이 숫자로 채워주세요.")
                        return
                    self.puzzle[i][j] = int(val)

        if self.is_valid_solution():
            messagebox.showinfo("성공", "정답입니다!")
        else:
            messagebox.showerror("오답", "틀린 칸이 있습니다.")

    def is_valid_solution(self):
        def check_group(group):
            return sorted(group) == list(range(1, 10))

        for i in range(9):
            if not check_group([self.puzzle[i][j] for j in range(9)]):
                return False
            if not check_group([self.puzzle[j][i] for j in range(9)]):
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                block = [self.puzzle[r][c] for r in range(box_row, box_row + 3)
                         for c in range(box_col, box_col + 3)]
                if not check_group(block):
                    return False
        return True

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = SudokuUI()
    game.run()
