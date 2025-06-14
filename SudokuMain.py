import tkinter as tk
from tkinter import messagebox
import random
from memo import Memo
from trans import Trans

# -------------------- Board Class --------------------
class Board:
    def __init__(self):
        # 9x9 스도쿠 보드 초기화 (모든 칸을 0으로 시작)
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.fixed_cells = set() # 고정된 셀 위치 저장

    def is_valid(self, row, col, num):
        # 특정 숫자가 해당 셀에 들어갈 수 있는지 확인 (현 보드를 기준으로 판단)
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        # 3x3 박스 안에서도 중복 없게
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.grid[box_row + i][box_col + j] == num:
                    return False

        return True

    def fill_grid(self):
        # 백트래킹 방식으로 완성된 스도쿠 생성
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
        # 퍼즐 생성 (완성된 스도쿠에서 일부 숫자 제거함)
        self.fill_grid() # 1. 완성된 정답 보드를 만듦
        puzzle = [row[:] for row in self.grid]
        attempts = 20 # 2. 셀을 몇 번 지워볼 건지 설정 (즉, 지우기 시도 횟수)

        while attempts > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)

            while puzzle[row][col] == 0: # 이미 빈 셀이면 패스
                row, col = random.randint(0, 8), random.randint(0, 8)

            backup = puzzle[row][col]
            puzzle[row][col] = 0 # 셀을 비운다
            copy = [r[:] for r in puzzle]

            if self.count_solutions(copy) != 1:
                puzzle[row][col] = backup # 지웠더니 정답이 1개가 아니면 다시 복원
                attempts -= 1 # 실패한 시도로 간주 → 시도 횟수 줄이기

        self.grid = puzzle
        self.fixed_cells = {(i, j) for i in range(9) for j in range(9) if puzzle[i][j] != 0}

    def count_solutions(self, grid):
        # 유효한 정답 개수 세기 (무조건 1개여야 함)
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
        # 해당 셀에 숫자 넣을 수 있는지 확인
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
        # 모든 셀이 채워졌는지 확인
        return all(all(cell != 0 for cell in row) for row in self.grid)

    def is_correct(self):
        # 입력 값이 스도쿠 규칙에 맞는 정답인지 확인
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
        # 고정 셀 말고 입력한 셀만 초기화
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.fixed_cells:
                    self.grid[i][j] = 0

    def set_cell(self, row, col, val):
        # 해당 셀에 값 삽입
        self.grid[row][col] = val


# -------------------- GameUI Class --------------------
class GameUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("스도쿠 게임")
        self.memo = Memo(self.root)  # 메모 기능 초기화
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.alpha_value = 1.0

        self.display_grid()

        # 화면 하단 버튼 배치
        tk.Button(self.root, text="셀 초기화", command=self.reset_board).grid(row=9, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="정답 확인", command=self.check_game).grid(row=9, column=3, columnspan=3, pady=10)
        tk.Button(self.root, text="메모 모드", command=lambda: self.memo.toggle_memo_mode(None)).grid(row=9, column=6, columnspan=3, pady=10)
        # 인자 있는 함수 호출 시엔 람다 사용(버튼을 누를 때 실행하도록)

        self.memo.set_entries(self.entries)  # 메모 기능에 entries 전달

        transparency_btn = tk.Button(self.root, text="투명도 조절창 열기", command=self.open_transparency_window)
        transparency_btn.grid(row=10, column=0, columnspan=9, pady=10)

    def open_transparency_window(self):
        Trans(self.root, self.alpha_value, self.set_alpha_value)  # 이제 이게 새로운 Toplevel 창 열어줌

    def set_alpha_value(self, val):
        self.alpha_value = val
        self.root.attributes('-alpha', val)

    def display_grid(self):
        # 보드 셀을 화면에 표시
        colors = ['#ffffff', '#e6f7ff'] # 격자 배경 색 번갈아 적용 (3x3 마다)
        board = self.game.board.grid
        for i in range(9):
            for j in range(9):
                color_index = ((i // 3) + (j // 3)) % 2
                bg_color = colors[color_index]  # 배경색 미리 지정

                entry = tk.Entry(self.root, width=2, font=("Arial", 16), justify="center", bg=bg_color)

                if (i, j) in self.game.board.fixed_cells:
                    entry.insert(0, str(board[i][j]))
                    entry.config(state="readonly", readonlybackground=bg_color, disabledforeground="black")
                else:
                    entry.bind("<KeyRelease>", lambda e, x=i, y=j: self.memo.handle_input(x, y))  # 메모 핸들링 추가

                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

    def reset_board(self):
        # 퍼즐 리셋 (입력된 셀만 초기화)
        self.game.board.reset_board()
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.game.board.fixed_cells:
                    self.entries[i][j].delete(0, tk.END)

    def check_game(self):
        # 사용자의 입력 값을 보드에 반영하고 정답 확인
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
        # 팝업 메세지 출력
        messagebox.showinfo(title, msg)

    def show_result_popup(self, message):
        # 재도전 또는 닫기 버튼 있는 Toplevel 창 띄워줌
        popup = tk.Toplevel(self.root)
        popup.title("결과")
        popup.geometry("250x120")
        popup.resizable(False, False)

        label = tk.Label(popup, text=message)
        label.pack(pady=10)

        # 버튼들 담을 프레임 생성(가로 배치 위해)
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        close_btn = tk.Button(button_frame, text="닫기", command=popup.destroy, bg="red", fg="white")
        close_btn.pack(side='left', padx=10)

        restart_btn = tk.Button(button_frame, text="재도전", command=lambda: self.restart_game(popup), bg="lightblue")
        restart_btn.pack(side='left', padx=10)

    def restart_game(self, popup_window):
        # 재도전 버튼 클릭 시 실행(새로운 스도쿠 생성)
        popup_window.destroy()  # 팝업 닫기
        self.root.destroy()  # 현재 게임 창 닫기

        # 새 게임 시작
        new_game = SudokuGame()
        new_game.start_game()

    def run(self):
        # UI 실행
        self.root.mainloop()


# -------------------- SudokuGame Class --------------------
class SudokuGame:
    def __init__(self):
        # 게임 초기화
        self.board = Board()
        self.ui = GameUI(self)

    def start_game(self):
        # 스도쿠 생성 후 UI 실행
        self.board.generate_puzzle()
        self.ui.display_grid()
        self.ui.run()

    def check_game_status(self):
        # 완성 및 정답 여부 확인
        if not self.board.is_complete():
            self.ui.show_message("미완성", "모든 칸을 입력해주세요.")
        elif self.board.is_correct():
            self.ui.show_result_popup("🎉 정답입니다!")
        else:
            self.ui.show_result_popup("❌ 오답입니다!")

#     def test_full_grid_gui(self):
#         # 완성된 스도쿠 보드 생성 (잘 생성 되는지 확인용)
#         self.board.fill_grid()  # 정답 보드 생성
#         # 모든 셀을 고정 셀로 처리해서 사용자가 수정 못하게
#         self.board.fixed_cells = {(i, j) for i in range(9) for j in range(9)}
#         self.ui.display_grid()
#         self.ui.run()
#
#
# if __name__ == "__main__":
#     game = SudokuGame()
#     game.test_full_grid_gui()  # 스도쿠 정답 보드를 GUI로 확인