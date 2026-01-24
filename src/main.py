import tkinter as tk

from boards import Board, AnalysisBoard
from players import HumanPlayer, Bot
from ui_helper import *

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

        # --- Boards ---
        canvas_frame = tk.Frame(self._root)
        canvas_frame.pack(padx=PADDING, pady=PADDING)

        ui_label(canvas_frame, "White Analysis", 13, column=0)
        ui_label(canvas_frame, "Live Board", 25, column=1)
        ui_label(canvas_frame, "Black Analysis", 13, column=2)
        canvases = [ui_square_canvas(canvas_frame, BOARD_SIZE,
                                     row=1, column=i, padding=PADDING)
                    for i in range(3)]
        self.white_board = AnalysisBoard(canvases[0])
        self.live_board = Board(canvases[1])
        self.black_board = AnalysisBoard(canvases[2])

        # --- Player controls ---
        bar = tk.Frame(self._root, bg="lightgray", height=50)
        bar.pack(side="top", fill="x", pady=PADDING, padx=PADDING)
        button_container = tk.Frame(bar, bg="lightgray")
        button_container.place(relx=0.5, rely=0.5, anchor="center")

        self._button = [None, None, None]
        self._button[0] = tk.Button(button_container, text="Trigger White Bot")
        self._button[1] = tk.Button(button_container, text="Undo 1 Ply")
        self._button[2] = tk.Button(button_container, text="Trigger Black Bot")
        self._button[0].pack(side="left", padx=PADDING, pady=PADDING)
        self._button[1].pack(side="left", padx=PADDING, pady=PADDING)
        self._button[2].pack(side="left", padx=PADDING, pady=PADDING)

        # --- Read-only scrolling text boxes for logging ---
        text_frame = tk.Frame(self._root, width=LOG_SIZE[0], height=LOG_SIZE[1])
        text_frame.pack(padx=PADDING, pady=(0, PADDING))
        text_frame.pack_propagate(False)

        inner = tk.Frame(text_frame)
        inner.pack(fill="both", expand=True)
        inner.rowconfigure(0, weight=1)

        self._game_log = ui_text_box(inner, column=0)
        self._analysis_log = ui_text_box(inner, column=1)

    def set_players(self, player1class, player2class):
        self.white = player1class(
            True,
            self.live_board,
            self.white_board,
            self.log_info
        )
        self.black = player2class(
            False,
            self.live_board,
            self.black_board,
            self.log_info
        )

    def begin(self):
        self._button[1].bind("<Button-1>", self.undo_ply, add="+")

        self.live_board.surface.bind("<Button-1>", self.white.on_click, add="+")
        self.live_board.surface.bind("<Button-1>", self.black.on_click, add="+")

        self.white_board.surface.bind("<Button-1>", self.white.on_analysis_click)
        self.black_board.surface.bind("<Button-1>", self.black.on_analysis_click)

        self._button[0].bind("<Button-1>", self.white.bot_trigger, add="+")
        self._button[2].bind("<Button-1>", self.black.bot_trigger, add="+")

        self._root.mainloop()


    # --- Callback functions ---
    def undo_ply(self, event):
        self.live_board.pop()
        self.live_board.render()

    def log_info(self, text, analysis=False):
        if not analysis:
            self._game_log.configure(state="normal")
            self._game_log.insert(tk.END, text)
            self._game_log.see(tk.END)
            self._game_log.configure(state="disabled")
        else:
            self._analysis_log.configure(state="normal")
            self._analysis_log.delete("1.0", tk.END)
            self._analysis_log.insert(tk.END, text)
            self._analysis_log.configure(state="disabled")

g = GameManager()
g.set_players(HumanPlayer, Bot)
g.begin()
