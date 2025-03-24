import cv2
import numpy as np
import tkinter as tk
from tkinter import Toplevel

import score

# python counterDebug.py 
# test pin counting system

root = tk.Tk()

numOfPlayers = 2 #make it an user input value in the future
currentPlayer = 0
currentFrame = 0

system = score.Score(root, numOfPlayers) #open bowling scoreboard and keep track/edit through system var



tk.mainloop()