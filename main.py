import cv2
import numpy as np
import tkinter as tk
from tkinter import Toplevel

import score

# python counterDebug.py 
# test pin counting system

root = tk.Tk()

score.Score(root) #open bowling scoreboard

tk.mainloop()