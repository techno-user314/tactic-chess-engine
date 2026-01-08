import chess

PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}
SQUARE_SIZE = 64
LIGHT_SQ = "#F0D9B5"
DARK_SQ = "#B58863"

class Board(chess.Board):
    def __init__(self, canvas):
        super().__init__()
        self.surface = canvas
        self.selected_square = None
        self.render()

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
                    fill=LIGHT_SQ if (row + col) % 2 != 0 else DARK_SQ,
                    outline=""
                )
                square = chess.square(col, 7 - row)
                piece = self.piece_at(square)
                if piece:
                    self.surface.create_text(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2,
                        text=PIECES[piece.symbol()],
                        font=("Arial", 36)
                    )
        if self.selected_square is not None:
            # Draw selection box
            col = chess.square_file(self.selected_square)
            row = 7 - chess.square_rank(self.selected_square)
            self.surface.create_rectangle(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                (col + 1) * SQUARE_SIZE,
                (row + 1) * SQUARE_SIZE,
                outline="#444444",
                width=3
            )

            # Draw legal moves for selected piece
            legal_moves_for_piece = [
                move for move in self.legal_moves
                if move.from_square == self.selected_square
            ]

            for move in legal_moves_for_piece:
                col = chess.square_file(move.to_square)
                row = 7 - chess.square_rank(move.to_square)

                cx = col * SQUARE_SIZE + SQUARE_SIZE // 2
                cy = row * SQUARE_SIZE + SQUARE_SIZE // 2

                if self.piece_at(move.to_square):
                    r = SQUARE_SIZE // 3
                    self.surface.create_oval(
                        cx - r, cy - r,
                        cx + r, cy + r,
                        outline="#0F0F0F",
                        width=2,
                    )
                else:
                    r = SQUARE_SIZE // 10
                    self.surface.create_oval(
                        cx - r, cy - r,
                        cx + r, cy + r,
                        fill="#000000",
                        outline="",
                        stipple="gray50"
                    )

    def play_move(self, move):
        if move in self.legal_moves:
            self.push(move)
            self.render()

class AnalysisBoard(Board):
    pass
