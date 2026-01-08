import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from boards import Board, AnalysisBoard
from players import HumanPlayer

BOARD_SIZE = 512 # Board display size in pixels
LOG_SIZE = (BOARD_SIZE * 3, 384)
PADDING = 5

class GameManager:
    def __init__(self):
        self.white = None
        self.black = None
        self.white_turn = True

        # --- Initialize gui ---
        self._root = tk.Tk()
        self._root.title("Chess - Bot Development")
        self._root.resizable(False, False)

        # Frame for labels and canvases
        canvas_frame = tk.Frame(self._root)
        canvas_frame.pack(padx=PADDING, pady=PADDING)

        # Board labels
        labels = ["White Analysis", "Live Board", "Black Analysis"]
        for i, label_text in enumerate(labels):
            label = tk.Label(
                canvas_frame,
                text=label_text,
                anchor="center",
                font=("Arial", 25 if i == 1 else 13)
            )
            label.grid(row=0, column=i, pady=(0, 2))

        # Board canvases row
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

        # Create read-only scrolling text box
        text_frame = tk.Frame(self._root, width=LOG_SIZE[0], height=LOG_SIZE[1])
        text_frame.pack(padx=PADDING, pady=(0, PADDING))
        text_frame.pack_propagate(False)

        self._analysis_log = ScrolledText(text_frame, wrap="word")
        self._analysis_log.pack(fill="both", expand=True)
        self._analysis_log.configure(state="disabled")

    def set_game(self):
        white_board = AnalysisBoard(self._canvases[0])
        live_board = Board(self._canvases[1])
        black_board = AnalysisBoard(self._canvases[2])

        self.white = HumanPlayer(
            True,
            live_board,
            white_board,
            self.log_info
        )
        self.black = HumanPlayer(
            False,
            live_board,
            black_board,
            self.log_info
        )

    def begin(self):
        self._root.after(1000, self.update_turn)
        self._root.mainloop()

    # --- Callback functions for the players ---
    def log_info(self, text):
        self._analysis_log.configure(state="normal")
        self._analysis_log.insert(tk.END, text)
        self._analysis_log.configure(state="disabled")

    def update_turn(self):
        if self.white_turn:
            self.white.move(self._root.after, (100, self.update_turn))
        else:
            self.black.move(self._root.after, (100, self.update_turn))
        self.white_turn = not self.white_turn

g = GameManager()
g.set_game()
g.begin()
