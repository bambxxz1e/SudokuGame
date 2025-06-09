import random

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.notes = [[set() for _ in range(9)] for _ in range(9)]
        self.fixed_cells = set()
        self.generate_puzzle()

    def generate_puzzle(self):
        # 간단한 초기 퍼즐 생성 (정답 확인은 생략)
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = 0
        self.fixed_cells = set()  # 임시로 비움

    def set_cell(self, row, col, value):
        if (row, col) not in self.fixed_cells:
            self.grid[row][col] = value

    def toggle_note(self, row, col, value):
        if value in self.notes[row][col]:
            self.notes[row][col].remove(value)
        else:
            self.notes[row][col].add(value)

    def clear_cell(self, row, col):
        if (row, col) not in self.fixed_cells:
            self.grid[row][col] = 0

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.fixed_cells:
                    self.grid[i][j] = 0

    def is_complete(self):
        return all(self.grid[i][j] != 0 for i in range(9) for j in range(9))

    def is_correct(self):
        # 정답 판별 로직은 생략 (필요 시 추가)
        return True
