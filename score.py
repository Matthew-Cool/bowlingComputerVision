import cv2
import numpy as np
import tkinter as tk
import tkinter.font as tkF

class Score:
    def __init__(self, root, requestPlayers):
        self.root = root
        self.root.title("Tabletop Bowling Scoreboard")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)

        self.currentPlayer = 0
        self.currentFrame = 0
        self.currentThrow = 0
        self.numOfPlayers = requestPlayers

        self.players = {str(i) : [tk.IntVar(), #0
            tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(), #1-10
            tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(), #11-20
            False, False] #21-22 , oneDouble and twoDouble
        for i in range(requestPlayers)}

        self.root.bind("<Return>", self.onKeyPress)

        titleFrame = tk.Frame(self.root, bg='black')
        titleLabel = tk.Label(titleFrame, text="Tabletop Bowling Scoreboard", font=("Arial", 20), fg="blue", bg='black')
        titleLabel.pack(pady=3)
        titleFrame.pack(pady=3, fill="x")

        scoreFrame = tk.Frame(self.root, bg='black')
        scoreFrame.pack(pady=3, fill="both")

        frameNumFrame = tk.Frame(scoreFrame, bg='black')
        frameNumFrame.pack(pady=3)

        self.createTopFrameNums(frameNumFrame)

        for i in range(requestPlayers):
            self.createFrames(scoreFrame, i)

    def createTopFrameNums(self, r):
        for i in range(11):
            text = tk.StringVar() #im lazy so its a textEntry becase of spacing is annoying me and im lazy, wait did I say that already?
            text.set(str(i+1))

            if i == 11:
                text = "Total:"

            tk.Entry(r, 
                width=10,
                textvariable=str(text), 
                state="disabled",
                disabledbackground="black",
                disabledforeground="white",
                borderwidth=0,
                highlightthickness=0,
                justify="center",
                font=tkF.Font(size=16)).pack(side=tk.LEFT,pady=10,padx=2)

    def createFrames(self, root, playerNum):
        playerFrame = tk.Frame(root, bg='black')
        playerFrame.pack(pady=3, padx=3)

        for i in range(10):
            self.frame(playerFrame, playerNum, i+11, i+1)

        totalFrame = tk.Frame(playerFrame, bg='white')
        totalFrame.pack(side=tk.LEFT, padx=3)

        totalOutLineFrame = tk.Frame(totalFrame, bg='black')
        totalOutLineFrame.pack(pady=2, padx=2)

        tk.Entry(totalOutLineFrame, 
                width=10,
                textvariable=self.players[str(playerNum)][0], 
                state="disabled",
                disabledbackground="black",
                disabledforeground="white",
                borderwidth=0,
                highlightthickness=0,
                justify="center",
                font=tkF.Font(size=16)).pack(pady=10)

    def frame(self, root, playerNum, frameTextNum, frameNumNum):
        titleFrame = tk.Frame(root, bg='white')
        titleFrame.pack(side=tk.LEFT)

        outLineFrame = tk.Frame(titleFrame, bg='black')
        outLineFrame.pack(pady=2, padx=2)

        tk.Entry(outLineFrame, 
                width=10,
                textvariable=self.players[str(playerNum)][frameTextNum], 
                state="disabled",
                disabledbackground="black",
                disabledforeground="white",
                borderwidth=0,
                highlightthickness=0,
                justify="center",
                font=tkF.Font(size=16)).pack(pady=10)
        tk.Entry(outLineFrame, 
                width=10,
                textvariable=self.players[str(playerNum)][frameNumNum], 
                state="disabled",
                disabledbackground="black",
                disabledforeground="white",
                borderwidth=0,
                highlightthickness=0,
                justify="center",
                font=tkF.Font(size=16)).pack(pady=10)

    def onKeyPress(self, event):
        self.checkScore()
            
    def updateScore(self, pins):
        player = self.players[str(self.currentPlayer)]

        if pins == 0:
            if self.currentThrow == 0:
                upperText = "X"
            else:
                upperText = f'{str(player[self.currentFrame+1].get())}     /'
        else:
            if self.currentThrow == 0:
                upperText = str(10-pins)
            else:
                upperText = f'{str(player[self.currentFrame+1].get())}     {str((10-pins) - player[self.currentFrame+1].get())}'
        
        #edit num score
        player[self.currentFrame+1].set(10-pins)
        player[self.currentFrame+11].set(upperText)
        

        self.updateValues()

    def updateValues(self):
        if self.currentPlayer >= self.numOfPlayers-1:
            self.currentPlayer = 0
            self.currentFrame += 1
            if self.currentThrow >= 1:
                self.currentThrow = 0
            else:
                self.currentThrow = 1
        elif self.currentThrow == 0:
            self.currentThrow = 1
        else:
            self.currentPlayer += 1
            self.currentThrow = 0
            
        print(f'currentPlayer={self.currentPlayer}\ncurrentFrame={self.currentFrame}\ncurrentThrow={self.currentThrow}')

    def checkScore(self):
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
        lowerWhite = np.array([0,0,253])
        upperWhite = np.array([180,5,255])

        mask = cv2.inRange(hsv, lowerWhite, upperWhite)

        result = cv2.bitwise_and(frame, frame, mask=mask)

        greyResult = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(greyResult, (1, 1), 0)
        _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filterFalsePositives = []
        for c in contours:
            area = cv2.contourArea(c)
            if 500 < area < 2000:
                filterFalsePositives.append(c)

        pins = len(filterFalsePositives)
        #END OF COUNTING SYSTEM

        cv2.drawContours(result, filterFalsePositives, -1, (255,0,0), 2)


        cv2.imwrite(img=result, filename='scorePhoto.jpg')

        cap.release()

        self.updateScore(pins)
