import tkinter as tk
from tkinter.scrolledtext import ScrolledText

def ui_label(parent, text, font_size, row=0, column=0, padding=0):
    label = tk.Label(
        parent,
        text=text,
        anchor="center",
        font=("Arial", font_size)
    )
    label.grid(row=row, column=column, padx=padding)
    return label

def ui_text_box(parent, row=0, column=0):
    tbox = ScrolledText(parent, wrap=tk.WORD)
    tbox.grid(row=row, column=column, sticky="nsew")
    tbox.configure(state="disabled")
    return tbox

def ui_square_canvas(parent, size, row=0, column=0, padding=0):
    c = tk.Canvas(
        parent, width=size, height=size,
        bg="lightgray", highlightthickness=1, highlightbackground="black"
    )
    c.grid(row=row, column=column, padx=padding)
    return c
