import chess
from boards import SQUARE_SIZE

PIECE_VALUES = {chess.PAWN:1,
                chess.KNIGHT:2.5,
                chess.BISHOP:3,
                chess.ROOK:5,
                chess.QUEEN:10,
                chess.KING:1000}

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

        self.move_finished = lambda a, b: a * b
        self.move_finished_args = (10, 20)

    def on_click(self, event):
        if self.play_board.is_game_over():
            self.log("Game Over\n")
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
                        self.move_finished(*self.move_finished_args)
                        break
                self.play_board.selected_square = None
                self.play_board.render()

    def move(self, callback, args):
        self.move_finished = callback
        self.move_finished_args = args

class Bot(Player):
    def __init__(self, is_white, live_board, analysis_board, logger):
        super().__init__(is_white, live_board, analysis_board, logger)
        self.move_scores = {}

    def move(self, callback, args):
        if self.play_board.is_game_over():
            self.log("Game Over\n")
            return
        if self.play_board.turn == self.color:
            self.log("Bot thinking...\n")
            for first_move in self.play_board.legal_moves:
                board_after_move = chess.Board(self.play_board.fen())
                board_after_move.push(first_move)
    
                pos_score = self.score_pos(board_after_move)
                self.move_scores.update({first_move:pos_score})
    
            best_move_score = max(self.move_scores.values())
            all_best_moves = [key for key, value in self.move_scores.items()
                              if value == best_move_score]
            self.play_board.play_move(all_best_moves[0])
            self.move_scores = {}
            callback(*args)

    def material_count(self, board_pos, for_opponent=False):
        for_color = not self.color if for_opponent else self.color
        mat_count = 0
        for piece_type in PIECE_VALUES.keys():
            piece_squares = board_pos.pieces(piece_type, for_color)
            mat_count += PIECE_VALUES[piece_type] * len(piece_squares)
        return mat_count

    def score_pos(self, board_pos):
        my_mat = self.material_count(board_pos)
        other_mat = self.material_count(board_pos, for_opponent=True)
        return my_mat - other_mat
