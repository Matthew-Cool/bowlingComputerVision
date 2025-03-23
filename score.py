import tkinter as tk
from tkinter import Toplevel

class Score:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabletop Bowling Scoreboard")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)

        titleFrame = tk.Frame(self.root, bg='black')
        titleLabel = tk.Label(titleFrame, text="Tabletop Bowling Scoreboard", font=("Arial", 20), fg="blue", bg='black')
        titleLabel.pack(pady=3)
        titleFrame.pack(pady=3, fill="x")
        