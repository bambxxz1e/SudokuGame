from Board import Board
from GameUI import GameUI

class SudokuGame:
    def __init__(self):
        self.board = Board()
        self.ui = GameUI(self)

    def start_game(self):
        self.board.reset_board()
        self.ui = GameUI(self)
        self.ui.run()

    def check_game_status(self):
        if self.board.is_complete():
            if self.board.is_correct():
                self.ui.show_message("축하합니다! 정답입니다!")
            else:
                self.ui.show_message("틀렸습니다. 다시 시도해 보세요.")
            self.ui.show_restart_button()
        else:
            self.ui.show_message("아직 완성되지 않았습니다.")

if __name__ == "__main__":
    game = SudokuGame()
    game.ui.run()