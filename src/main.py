import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from boards import Board, AnalysisBoard
from players import HumanPlayer, Bot

BOARD_SIZE = 432 # Board display size in pixels
LOG_SIZE = (BOARD_SIZE * 3, 320)
PADDING = 5

class GameManager:
    def __init__(self):
        self.white = None
        self.black = None

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

        # Button bar
        bar = tk.Frame(self._root, bg="lightgray", height=50)
        bar.pack(side="top", fill="x", pady=PADDING, padx=PADDING)
        button_container = tk.Frame(bar, bg="lightgray")
        button_container.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons
        self._button = [None, None, None]
        self._button[0] = tk.Button(button_container, text="Trigger White Bot")
        self._button[1] = tk.Button(button_container, text="Undo 1 Ply")
        self._button[2] = tk.Button(button_container, text="Trigger Black Bot")
        self._button[0].pack(side="left", padx=PADDING, pady=PADDING)
        self._button[1].pack(side="left", padx=PADDING, pady=PADDING)
        self._button[2].pack(side="left", padx=PADDING, pady=PADDING)

        # Read-only scrolling text box for logging
        text_frame = tk.Frame(self._root, width=LOG_SIZE[0], height=LOG_SIZE[1])
        text_frame.pack(padx=PADDING, pady=(0, PADDING))
        text_frame.pack_propagate(False)

        #self._analysis_log = ScrolledText(text_frame, wrap="word")
        #self._analysis_log.pack(fill="both", expand=True)
        #self._analysis_log.configure(state="disabled")

        # Use grid inside this frame
        inner = tk.Frame(text_frame)
        inner.pack(fill="both", expand=True)
        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        inner.rowconfigure(0, weight=1)

        self._game_log = ScrolledText(inner, wrap="word")
        self._game_log.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self._game_log.configure(state="disabled")

        self._analysis_log = ScrolledText(inner, wrap="word")
        self._analysis_log.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self._analysis_log.configure(state="disabled")

    def set_players(self, player1class, player2class):
        white_board = AnalysisBoard(self._canvases[0])
        live_board = Board(self._canvases[1])
        black_board = AnalysisBoard(self._canvases[2])

        self.white = player1class(
            True,
            live_board,
            white_board,
            self._button,
            self.log_info
        )
        self.black = player2class(
            False,
            live_board,
            black_board,
            self._button,
            self.log_info
        )

    def begin(self):
        self._root.mainloop()

    # --- Callback functions for the players ---
    def log_info(self, text, analysis=False):
        if not analysis:
            self._game_log.configure(state="normal")
            self._game_log.insert(tk.END, text)
            self._game_log.configure(state="disabled")
        else:
            self._analysis_log.configure(state="normal")
            self._analysis_log.delete("1.0", tk.END)
            self._analysis_log.insert(tk.END, text)
            self._analysis_log.configure(state="disabled")

g = GameManager()
g.set_players(HumanPlayer, Bot)
g.begin()
