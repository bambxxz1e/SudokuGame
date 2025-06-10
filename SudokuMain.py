import tkinter as tk
from tkinter import messagebox
import random
from memo import Memo

# -------------------- Board Class --------------------
class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.fixed_cells = set()

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

    def generate_puzzle(self):
        self.fill_grid()
        puzzle = [row[:] for row in self.grid]
        attempts = 30
        while attempts > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while puzzle[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            copy = [r[:] for r in puzzle]
            if self.count_solutions(copy) != 1:
                puzzle[row][col] = backup
                attempts -= 1

        self.grid = puzzle
        self.fixed_cells = {(i, j) for i in range(9) for j in range(9) if puzzle[i][j] != 0}

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

    def is_complete(self):
        return all(all(cell != 0 for cell in row) for row in self.grid)

    def is_correct(self):
        def check_group(group):
            return sorted(group) == list(range(1, 10))

        for i in range(9):
            if not check_group([self.grid[i][j] for j in range(9)]):
                return False
            if not check_group([self.grid[j][i] for j in range(9)]):
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                block = [self.grid[r][c] for r in range(box_row, box_row + 3)
                         for c in range(box_col, box_col + 3)]
                if not check_group(block):
                    return False
        return True

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.fixed_cells:
                    self.grid[i][j] = 0

    def set_cell(self, row, col, val):
        self.grid[row][col] = val


# -------------------- GameUI Class --------------------
class GameUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("스도쿠 게임")
        self.memo = Memo(self.root)  # 메모 기능 추가
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        self.display_grid()

        tk.Button(self.root, text="초기화", command=self.reset_board).grid(row=9, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="정답 확인", command=self.check_game).grid(row=9, column=3, columnspan=3, pady=10)
        tk.Button(self.root, text="메모 모드", command=lambda: self.memo.toggle_memo_mode(None)).grid(row=9, column=6, columnspan=3, pady=10)

        self.memo.set_entries(self.entries)  # 메모 기능에 entries 전달

    def display_grid(self):
        colors = ['#ffffff', '#e6f7ff']
        board = self.game.board.grid
        for i in range(9):
            for j in range(9):
                color_index = ((i // 3) + (j // 3)) % 2
                entry = tk.Entry(self.root, width=2, font=("Arial", 16), justify="center", bg=colors[color_index])
                if (i, j) in self.game.board.fixed_cells:
                    entry.insert(0, str(board[i][j]))
                    entry.config(state="readonly", disabledforeground="black")
                else:
                    entry.bind("<KeyRelease>", lambda e, x=i, y=j: self.memo.handle_input(x, y))  # 메모 핸들링 추가

                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

    def reset_board(self):
        self.game.board.reset_board()
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.game.board.fixed_cells:
                    self.entries[i][j].delete(0, tk.END)

    def check_game(self):
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.game.board.fixed_cells:
                    val = self.entries[i][j].get()
                    if not val.isdigit() or not (1 <= int(val) <= 9):
                        self.show_message("오류", "모든 칸을 1~9 사이 숫자로 채워주세요.")
                        return
                    self.game.board.set_cell(i, j, int(val))

        self.game.check_game_status()

    def show_message(self, title, msg):
        messagebox.showinfo(title, msg)

    def run(self):
        self.root.mainloop()


# -------------------- SudokuGame Class --------------------
class SudokuGame:
    def __init__(self):
        self.board = Board()
        self.ui = GameUI(self)

    def start_game(self):
        self.board.generate_puzzle()
        self.ui.display_grid()
        self.ui.run()

    def check_game_status(self):
        if not self.board.is_complete():
            self.ui.show_message("미완성", "모든 칸을 입력해주세요.")
        elif self.board.is_correct():
            self.ui.show_message("성공", "정답입니다!")
        else:
            self.ui.show_message("오답", "틀린 칸이 있습니다.")


# -------------------- Main 실행 --------------------
if __name__ == "__main__":
    game = SudokuGame()
    game.start_game()