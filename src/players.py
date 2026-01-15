from random import choice as pick_from
import chess
from boards import SQUARE_SIZE

PIECE_VALUES = {chess.PAWN:1,
                chess.KNIGHT:2.5,
                chess.BISHOP:3,
                chess.ROOK:5,
                chess.QUEEN:10,
                chess.KING:1000}
BOT_DEPTH_PLY = 2


class Player:
    def __init__(self, is_white, live_board, controls, logger):
        self.color = is_white
        self.play_board = live_board
        self.log = logger

        controls[1].bind("<Button-1>", self.undo_ply, add="+")

        if self.color: self.log("White player created\n")
        else: self.log("Black player created\n")

    def is_my_turn(self):
        if self.play_board.is_game_over():
            self.log("Game Over\n")
            return False
        elif self.play_board.turn == self.color:
            return True
        return False

    def click_board(self, board, click_x, click_y):
        col = click_x // SQUARE_SIZE
        row = click_y // SQUARE_SIZE
        square = chess.square(col, 7 - row)
        piece = board.piece_at(square)
        piece = piece if piece and piece.color == self.color else None
        if board.selected_square is not None:
            for move in board.legal_moves:
                if move.from_square == board.selected_square \
                        and move.to_square == square:
                    board.play_move(move)
                    break
        board.selected_square = square if piece else None
        board.render()

    def undo_ply(self, event):
        if self.color and self.play_board.ply() > 0:
            self.play_board.pop()
            self.play_board.render()


class HumanPlayer(Player):
    def __init__(self, is_white, live_board, analysis_board, controls, logger):
        super().__init__(is_white, live_board, controls, logger)
        self.play_board.surface.bind("<Button-1>", self.on_click, add="+")

    def on_click(self, event):
        if self.is_my_turn():
            self.click_board(self.play_board, event.x, event.y)


class Bot(Player):
    def __init__(self, is_white, live_board, analysis_board, controls, logger):
        super().__init__(is_white, live_board, controls, logger)
        trigger_button = 2 - int(self.color) * 2
        controls[trigger_button].bind("<Button-1>", self.bot_trigger, add="+")
        controls[trigger_button].bind("<Button-1>", self.bot_trigger, add="+")

        self.analysis_board = analysis_board
        self.analysis_board.surface.bind("<Button-1>", self.on_analysis_click)

        self.move_scores = {}
        self._search_calls = 0

    # --- Event response ---
    def bot_trigger(self, event):
        if self.is_my_turn():
            self.play_best_move()

    def on_analysis_click(self, event):
        if self.move_scores:
            self.click_board(self.analysis_board, event.x, event.y)

    # --- Finding and playing a move ---
    def get_move_score(self, move, board, depth):
        self._search_calls += 1
        board.push(move)
        if depth == 0 or board.is_game_over():
            best = self.evaluate_pos(board)
        else:
            best = -1e9 if board.turn == self.color else 1e9
            chooser = max if board.turn == self.color else min
            for next_move in board.legal_moves:
                score = self.get_move_score(next_move, board, depth - 1)
                best = chooser(best, score)
        board.pop()
        return best

    def play_best_move(self):
        self.move_scores = {}
        test_board = chess.Board(self.play_board.fen())
        self._search_calls = 0
        for move in self.play_board.legal_moves:
            score = self.get_move_score(move, test_board, BOT_DEPTH_PLY)
            self.move_scores.update({move.uci():score})
        best_move_score = max(self.move_scores.values())
        all_good_moves = [key for key, value in self.move_scores.items()
                          if value == best_move_score]
        best_move = chess.Move.from_uci(pick_from(all_good_moves))

        # Log move search info
        self.log(f"{"White" if self.color else "Black"} bot"
                 + f" picked {self.play_board.san(best_move)} randomly"
                 + f" out of {len(all_good_moves)} considered moves."
                 + f"\n    - It took {self._search_calls} recursions"
                 + f" at depth {BOT_DEPTH_PLY}.\n")
        alog_text = f"{"White" if self.color else "Black"} considered"
        for move in all_good_moves:
            m = chess.Move.from_uci(move)
            m = self.play_board.san(m)
            alog_text += f"\n    - {m}"
        self.log(alog_text, True)

        # Sync the analysis board with the current position minus last move
        self.analysis_board.set_fen(self.play_board.fen())
        self.analysis_board.set_scores(self.move_scores)
        self.analysis_board.selected_square = best_move.from_square
        self.analysis_board.render()

        self.play_board.play_move(best_move)

    # --- Helper functions ---
    def material_count(self, board_pos, for_opponent=False):
        for_color = not self.color if for_opponent else self.color
        mat_count = 0
        for piece_type in PIECE_VALUES.keys():
            piece_squares = board_pos.pieces(piece_type, for_color)
            mat_count += PIECE_VALUES[piece_type] * len(piece_squares)
        return mat_count

    # --- Position scoring logic ---
    # Override this method to customize the bot
    def evaluate_pos(self, board):
        my_mat = self.material_count(board)
        other_mat = self.material_count(board, for_opponent=True)
        return my_mat - other_mat
