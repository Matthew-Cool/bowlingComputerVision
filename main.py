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


def checkScore():
    # COUNTING SYSTEM
    frameWidth = 1280
    frameHeight = 720
    camBrightness = 150

    cap = cv2.VideoCapture(0)

    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, camBrightness)

    r, frame = cap.read()

    if not r: #something went wrong
        print('couldnt get capture')
        return
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerWhite = np.array([0,0,220])
    upperWhite = np.array([180,20,255])

    mask = cv2.inRange(hsv, lowerWhite, upperWhite)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    greyResult = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(greyResult, (9, 9), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filterFalsePositives = []
    for c in contours:
        area = cv2.contourArea(c)
        if 500 < area < 2000:
            filterFalsePositives.append(c)

    pins = len(filterFalsePositives)
    #END OF COUNTING SYSTEM

    cap.release()

    return pins





