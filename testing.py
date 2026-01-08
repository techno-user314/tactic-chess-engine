import random
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import chess

from boards import Board

BOARD_SIZE = 512 # Board display size in pixels
LOG_SIZE = (BOARD_SIZE * 3, 384)
PADDING = 5

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

class Player:
    def __init__(self):
        self.move_function = None
        self.analysis_board = None
        self.analysis_log = None

    def start_analysis_board(self, canvas, log):
        self.analysis_board = Board(canvas)
        self.analysis_board.render()
        self.analysis_log = log

    def log_info(self, message):
        self.analysis_log.configure(state="normal")
        self.analysis_log.insert("end", message + "\n")
        self.analysis_log.see("end")
        self.analysis_log.configure(state="disabled")

class Game:
    def __init__(self, player1, player2):
        self.board = None
        self.white = player1
        self.black = player2
        self.white_turn = True

        # Initialize gui
        self._root = tk.Tk()
        self._root.title("Chess - Bot Development")
        self._root.resizable(False, False)

        # --- Frame for labels and canvases ---
        canvas_frame = tk.Frame(self._root)
        canvas_frame.pack(padx=PADDING, pady=PADDING)

        # --- Labels row ---
        labels = ["White Analysis", "Live Board", "Black Analysis"]
        for i, label_text in enumerate(labels):
            label = tk.Label(
                canvas_frame,
                text=label_text,
                anchor="center",
                font=("Arial", 25 if i == 1 else 13)
            )
            label.grid(row=0, column=i, pady=(0, 2))

        # --- Canvases row ---
        self._canvases = [tk.Canvas(
            canvas_frame,
            width=BOARD_SIZE,
            height=BOARD_SIZE,
            bg="lightgray",
            highlightthickness=1,
            highlightbackground="black"
        ) for _ in range(3)]

        for i, c in enumerate(self._canvases):
            c.grid(row=1, column=i, padx=PADDING)

        # --- Create read-only scrolling text box ---
        text_frame = tk.Frame(self._root, width=LOG_SIZE[0], height=LOG_SIZE[1])
        text_frame.pack(padx=PADDING, pady=(0, PADDING))
        text_frame.pack_propagate(False)

        self._analysis_log = ScrolledText(text_frame, wrap="word")
        self._analysis_log.pack(fill="both", expand=True)
        self._analysis_log.configure(state="disabled")

    def start(self):
        self.white.start_analysis_board(self._canvases[0], self._analysis_log)
        self.black.start_analysis_board(self._canvases[2], self._analysis_log)

        self.board = Board(self._canvases[1])
        self.board.render()
        self._root.mainloop()

g = Game(Player(), Player())
g.start()
