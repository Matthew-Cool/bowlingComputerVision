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
        self.lastThrow = 0

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

            if i == 10:
                text.set("Total:")
            else:
                text.set(str(i+1))

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
        intIndex = self.currentFrame + 1
        textIndex = self.currentFrame + 11
        total = player[0].get()

        if self.currentFrame < 9: #frames 1-9
            if self.currentThrow == 0:
                if pins == 10: #strike
                    player[intIndex].set(10 + total)
                    player[textIndex].set('X')
                    self.nextPlayer()
                else: #not strike
                    player[intIndex].set(pins + total)
                    self.lastThrow = pins
                    player[textIndex].set(str(pins))
                    self.nextThrow()
                self.updatePlayerTotal(player, pins)
            else:
                if pins == 10: #spare
                    player[intIndex].set(10 - self.lastThrow + total)
                    player[textIndex].set(f'{player[textIndex].get()}   /')
                    self.nextPlayer()
                else: #not spare
                    player[intIndex].set(pins - self.lastThrow + total)
                    player[textIndex].set(f'{player[textIndex].get()}   {pins-self.lastThrow}')
                    self.nextPlayer()
                self.updatePlayerTotal(player, pins-self.lastThrow)
                self.lastThrow = -1000 #temp thing to check if I'm making mistakes lol
        else: #tenth frame
            if self.currentThrow == 0:
                if pins == 10: #strike 1
                    player[intIndex].set(10 + total)
                    player[textIndex].set('X')
                    self.lastThrow = 10
                    self.nextThrow()
                else: #not first strike
                    player[intIndex].set(pins + total)
                    self.lastThrow = pins
                    player[textIndex].set(str(pins))
                    self.nextThrow()
                self.updatePlayerTotal(player, pins)
            elif self.currentThrow == 1: 
                if self.lastThrow == 10 and pins == 10: #2nd strike
                    player[intIndex].set(10 + total)
                    player[textIndex].set(f'{player[textIndex].get()}   X')
                    self.lastThrow = 10
                    self.updatePlayerTotal(player, 10)
                    self.nextThrow()
                elif self.lastThrow != 10 and pins == 10: #1st spare
                    player[intIndex].set(10 - self.lastThrow + total)
                    player[textIndex].set(f'{player[textIndex].get()}   /')
                    self.lastThrow = -1
                    self.updatePlayerTotal(player, 10 - self.lastThrow)
                    self.nextThrow()
                else: #1st open, end game
                    player[intIndex].set(pins - self.lastThrow + total)
                    player[textIndex].set(f'{player[textIndex].get()}   {10 - self.lastThrow}')
                    self.lastThrow = -2
                    self.updatePlayerTotal(player, 10 - self.lastThrow)
                    self.nextPlayer()
            else: #last throw, end game no matter what
                if self.lastThrow == 10 and pins == 10: #3rd strike
                    player[intIndex].set(10 + total)
                    player[textIndex].set(f'{player[textIndex].get()}   X')
                    self.lastThrow = -3
                    self.updatePlayerTotal(player, 10)
                    self.nextPlayer()
                elif self.lastThrow != 10 and pins == 10:
                    player[intIndex].set(10 - self.lastThrow + total)
                    player[textIndex].set(f'{player[textIndex].get()}   /')
                    self.lastThrow = -4
                    self.updatePlayerTotal(player, 10 - self.lastThrow)
                    self.nextPlayer()
                else:
                    player[intIndex].set(pins - self.lastThrow + total)
                    player[textIndex].set(f'{player[textIndex].get()}   {10 - self.lastThrow}')
                    self.lastThrow = -5
                    self.updatePlayerTotal(player, 10 - self.lastThrow)
                    self.nextPlayer()

        print(f'currentPlayer={self.currentPlayer}\ncurrentFrame={self.currentFrame}\ncurrentThrow={self.currentThrow}')

    def nextThrow(self):
        if self.currentFrame <= 8: #we're on frames 1-9
            if self.currentThrow >= 1:
                self.currentThrow = 0
            else:
                self.currentThrow = 1
        else: #we're in the 10th frame
            if self.currentThrow >= 2:
                self.currentThrow = 0
            else:
                self.currentThrow += 1

    def nextFrame(self):
        if self.currentFrame >= 10:
            pass #end game somehow
        else:
            self.currentFrame += 1

    def nextPlayer(self):
        if self.currentPlayer >= self.numOfPlayers - 1:
            self.currentPlayer = 0
            self.currentThrow = 0
            self.nextFrame()
        else:
            self.currentPlayer += 1
            self.currentThrow = 0

    def updatePlayerTotal(self, player, addPins):
        player[0].set(player[0].get() + addPins)

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
        lowerWhite = np.array([0,0,250])
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

        pins = 10 - len(filterFalsePositives)
        #END OF COUNTING SYSTEM

        cv2.drawContours(result, filterFalsePositives, -1, (255,0,0), 2)


        cv2.imwrite(img=result, filename='scorePhoto.jpg')

        cap.release()

        print(f'pins={pins}')
        self.updateScore(pins)
