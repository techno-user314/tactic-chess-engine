import tkinter as tk
import chess

class Board:
    def __init__(self, canvas):
        self.board = chess.Board()
        self.surface = canvas

    def render(self):
        # Draw the board and pieces
        self.surface.delete("all")
        for row in range(8):
            for col in range(8):
                self.surface.create_rectangle(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    col * SQUARE_SIZE + SQUARE_SIZE,
                    row * SQUARE_SIZE + SQUARE_SIZE,
                    fill=LIGHT_SQ if (row + col) % 2 == 0 else DARK_SQ,
                    outline=""
                )
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                if piece:
                    self.surface.create_text(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2,
                        text=PIECES[piece.symbol()],
                        font=PIECE_FONT
                    )

class LiveBoard(Board):
  pass

class BotAnalysis(Board):
  pass
