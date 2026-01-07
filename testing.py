import tkinter as tk
import random

import chess

PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}
PIECE_FONT = ("Arial", 36)

SQUARE_SIZE = 64
LIGHT_SQ = "#F0D9B5"
DARK_SQ  = "#B58863"

def get_random_board():
    board = chess.Board()
    num_moves = 10
    for _ in range(num_moves):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            break
        random_move = random.choice(legal_moves)
        board.push(random_move)
    return board

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

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Chess")

    canvas = tk.Canvas(
        window, width=8 * SQUARE_SIZE, height=8 * SQUARE_SIZE
    )
    canvas.pack()

    b = Board(canvas)
    b.board = get_random_board()
    b.render()
    window.mainloop()
