import tkinter as tk
from tkinter import ttk

from boards import Board, AnalysisBoard
from players import HumanPlayer, Bot
from bot_loader import get_bots
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
        self._bots = get_bots()
        player_names = ["HumanPlayer"] + list(self._bots.keys())

        controls_bar = tk.Frame(self._root, height=50)
        controls_bar.pack(side="top", fill="x", pady=PADDING, padx=PADDING)
        controls_bar.grid_propagate(False)
        for i in range(5):
            controls_bar.grid_columnconfigure(i, weight=2 if i%4==0 else 1)

        self.white_btn = ttk.Button(controls_bar, text="Trigger White Bot")
        self.white_btn.grid(row=0, column=1)

        self.undo_btn = ttk.Button(controls_bar, text="Undo 1 Ply")
        self.undo_btn.grid(row=0, column=2)

        self.black_btn = ttk.Button(controls_bar, text="Trigger Black Bot")
        self.black_btn.grid(row=0, column=3)

        self.white_combo = ttk.Combobox(controls_bar, values=player_names,
                                   state="readonly", width=25)
        self.white_combo.grid(row=0, column=0, padx=PADDING)
        self.white_combo.current(0)

        self.black_combo = ttk.Combobox(controls_bar, values=player_names,
                                    state="readonly", width=25)
        self.black_combo.grid(row=0, column=4, padx=PADDING)
        self.black_combo.current(0)

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
        self.undo_btn.bind("<Button-1>", self.undo_ply, add="+")

        self.live_board.surface.bind("<Button-1>", self.white.on_click, add="+")
        self.live_board.surface.bind("<Button-1>", self.black.on_click, add="+")

        self.white_board.surface.bind("<Button-1>", self.white.on_analysis_click)
        self.black_board.surface.bind("<Button-1>", self.black.on_analysis_click)

        self.white_btn.bind("<Button-1>", self.white.bot_trigger, add="+")
        self.black_btn.bind("<Button-1>", self.black.bot_trigger, add="+")

        self._root.mainloop()


    # --- Callback functions ---
    def undo_ply(self, event):
        if self.live_board.ply() > 0:
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
