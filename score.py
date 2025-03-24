import tkinter as tk
from tkinter import Toplevel
import tkinter.font as tkF

class Score:
    def __init__(self, root, requestPlayers):
        self.root = root
        self.root.title("Tabletop Bowling Scoreboard")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)

        self.players = {str(i) : [tk.IntVar(), #0
            tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(), #1-10
            tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(), #11-20
            False, False] #21-22 , oneDouble and twoDouble
        for i in range(requestPlayers)}

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

        #self.players['1'][0].set(300)

    def createTopFrameNums(self, r):
        for i in range(10):
            text = tk.StringVar() #im lazy so its a textEntry becase of spacing is annoying me and im lazy, wait did I say that already?
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

        