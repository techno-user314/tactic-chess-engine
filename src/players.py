import chess
from boards import SQUARE_SIZE

class Player:
    def __init__(self, is_white, live_board, analysis_board, logger):
        self.color = is_white
        self.play_board = live_board
        self.log = logger

        if self.color: self.log("White player created\n")
        else: self.log("Black player created\n")

    def move(self, callback, args):
        pass

class HumanPlayer(Player):
    def __init__(self, is_white, live_board, analysis_board, logger):
        super().__init__(is_white, live_board, analysis_board, logger)
        self.play_board.surface.bind("<Button-1>", self.on_click, add="+")

        self.move_finished = None
        self.move_finished_args = None

    def on_click(self, event):
        if self.play_board.is_game_over():
            self.log("Game Over")
            return
        if self.play_board.turn == self.color:
            col = event.x // SQUARE_SIZE
            row = event.y // SQUARE_SIZE
            square = chess.square(col, 7 - row)

            if self.play_board.selected_square is None:
                piece = self.play_board.piece_at(square)
                if piece and piece.color == self.color:
                    self.play_board.selected_square = square
                    self.play_board.render()
            else:
                for move in self.play_board.legal_moves:
                    if move.from_square == self.play_board.selected_square \
                            and move.to_square == square:
                        self.play_board.play_move(move)
                        break
                self.play_board.selected_square = None
                self.play_board.render()
                self.move_finished(*self.move_finished_args)
            return

    def move(self, callback, args):
        self.move_finished = callback
        self.move_finished_args = args

class Bot(Player):
    pass
