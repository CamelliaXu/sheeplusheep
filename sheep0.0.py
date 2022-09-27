from cmu_112_graphics_openCV import *
import cv2
import numpy as np
# import mediapipe as mp
from PIL import Image as Img
import PIL
from tkinter import *
from Board import *


def appStarted(app):
    app.startBg = Img.open(r"hackstartbg.png")
    app.startBg = app.scaleImage(app.startBg, 1/2)
    app.bg = Img.open(r"bg.png")
    app.bg = app.scaleImage(app.bg, 1/2)
    app.startGame = False
    app.instruction = False
    app.realGame = False
    app.openCV = False
    app.isGameOver = False

    app.drawRanking = False
    app.score = 0
    app.sheepName =  None
    app.highScore = []
    app.button = Img.open(r"closeButton.png")
    app.button = app.scaleImage(app.button, 1/10)

    app.timerDelay = 10

    sprites = Img.open(r"quickSheeps.png")
    app.sprites = []
    for i in range(7):
        sprite = sprites.crop((0+107*i, 0, 100+107*i, 100))
        app.sprites.append(sprite)
    app.spriteCounter = 0
    app.sheepx = 500
    app.sheepy = 600
    app.runSpeed = 12

    app.cardPics = []
    for i in range (10):
        cardPic = Img.open(rf"{i}.png")
        cardPic = app.scaleImage(cardPic, 1/24)
        app.cardPics.append(cardPic)
    
    app.cardPicsUnder = []
    for i in range (10):
        newi = i + 10
        cardPic = Img.open(rf"{newi}.png")
        cardPic = app.scaleImage(cardPic, 1/24)
        app.cardPicsUnder.append(cardPic)


    app.x,app.y = (500,0)
    app.finger1x,app.finger1y = (500,0)
    app.finger2x,app.finger2y = (500,0)
    app.pickx,app.picky = (500,0)


    app.board = Board(5, 80)
    app.board.fillBoard()

    app.chosenCard = None

def chooseCard(app, event):
    (x, y) = (event.x, event.y)
    for i in range(app.board.level):
        currLayer = app.board.cardList[i]
        for card in currLayer:
            if card.isTop:
                if (x >= card.upleftX and x <= card.upleftX+80
                    and y >= card.upleftY and y <= card.upleftY+80):
                    app.chosenCard = card
        if app.chosenCard != None and app.chosenCard in app.board.cardList[i]:
            app.board.cardList[i].remove(app.chosenCard)
            app.board.updateDeck(app, app.chosenCard)

def chooseCardCV(app):
    (x, y) = (app.pickx, app.picky)
    for i in range(app.board.level):
        currLayer = app.board.cardList[i]
        for card in currLayer:
            if card.isTop:
                if (x >= card.upleftX+20 and x <= card.upleftX+60
                    and y >= card.upleftY+20 and y <= card.upleftY+60):
                    app.chosenCard = card
        if app.chosenCard != None and app.chosenCard in app.board.cardList[i]:
            app.board.cardList[i].remove(app.chosenCard)
            app.board.cardDeck.append(app.chosenCard)

def sameLevelNoOverlap(app, c):
    result = True
    for i in range(c.layer+1):
        currLayer = app.board.cardList[i]
        for card in currLayer:
            if c.overlap(card):
                return False
        return True
    # for i in range(app.board.level):
    #     currLayer = app.board.cardList[i]
    #     for card2 in currLayer:
    #         if card2.isTop and card2.overlap(c):
    #             result = False
    return result

def updateTop(app):
    if app.chosenCard != None:
        prevLayer = app.chosenCard.layer
        if prevLayer < app.board.level-1:
            currLayer = prevLayer + 1
        else: currLayer = app.board.level - 1
        for compareCard in app.board.cardList[currLayer]:
            if compareCard.overlap(app.chosenCard) and sameLevelNoOverlap(app, compareCard):
                compareCard.isTop = True

def distance(x1,y1,x2,y2):
    distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return distance

def mousePressed(app,event):
    startGame(app,event)
    instruction(app,event)
    newGame(app,event)
    openCV(app,event)
    chooseCard(app, event)
    updateTop(app)

def startGame(app,event):
    if (event.x > 420 and event.x < 555 and event.y > 380 and event.y < 425):
        app.startGame = True
    if (event.x > 600 and event.x < 1000 and event.y > 0 and event.y < 100):
        app.drawRanking = True
        updateHighScore(app)
    if (event.x > 715 and event.x < 725 and event.y > 220 and event.y < 230):
        app.drawRanking = False
         
def instruction(app,event):
    if (event.x > 355 and event.x < 645 and event.y > 575 and event.y < 665
    and app.startGame):
        app.instruction = True

def newGame(app,event):
    if (event.x > 400 and event.x < 600 and event.y > 450 and event.y < 550
    and app.startGame and app.instruction and app.realGame):
        appStarted(app)

# learn from section.io/engineering-education/creating-a-hand-tracking-module/
# def recognizeHand(app):
#     mpHands = mp.solutions.hands
#     hands = mpHands.Hands()
#     mpDraw = mp.solutions.drawing_utils
#     results = hands.process(app.frame)
#     if results.multi_hand_landmarks: #if detect a hand
#         for handLms in results.multi_hand_landmarks: # working with each hand
#             for id, lm in enumerate(handLms.landmark):
#                 h, w, c = app.frame.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h) #getting position of hand
#                 if id == 20 or id == 16 or id == 12 or id == 8 or id == 4:
#                     app.x,app.y = cx*4, 100 + cy*4
#                 if id == 4:
#                     app.finger1x,app.finger1y = cx*4, 100 + cy*4
#                 if id == 8:
#                     app.finger2x,app.finger2y = cx*4, 100 + cy*4
#                 if distance(app.finger1x,app.finger1y,app.finger2x,app.finger2y) < 40:
#                     app.pickx,app.picky = app.x,app.y

def openCV(app,event):
    if (event.x > 30 and event.x < 170 and event.y > 40 and event.y < 60
    and app.startGame):
        app.openCV = True

def cameraFired(app): 
    #resize & flip
    app.frame = cv2.resize(app.frame, dsize=(175, 100), interpolation=cv2.INTER_CUBIC)
    app.frame = cv2.flip(app.frame, 1)
    # if app.openCV:
    #     recognizeHand(app)
    #     chooseCardCV(app)

def timerFired(app):
    #sprite
    if not app.startGame:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.sprites)
    app.sheepx += app.runSpeed

def addScore(app):
    if app.isGameOver:
        choice = app.getUserInput("Hi do you want to store your score? YES or NO (DONT CANCEL)")
        if choice.upper() == "YES":
            app.sheepName = app.getUserInput("What is the sheep's name?")
            f = open("score.txt","a")
            f.write(f"{app.sheepName},{app.score},end")
        elif choice.upper() == "NO":
            app.sheepName =  None


def updateHighScore(app):
    score = open("score.txt", "r")
    allScore = score.read().strip()
    players = {}
    for oneplay in allScore.split("end"):
        if oneplay != "":
            playerName = oneplay.split(",")[0].strip()
            playerScore = oneplay.split(",")[1].strip()
            players[playerName] = playerScore
    L = [] #list of scores from high to low
    for playerName in players:
        score = players[playerName]
        L.append(int(score))
    L = sorted(L)
    L.reverse()
    for score in L:
        for playerName in players:
            if app.i < len(L) and app.i < 5:
                if int(players[playerName]) == score:
                    app.highScore.append((playerName,score))
                    app.i += 1


def drawSheep(app,canvas ):
    sprite = app.sprites[app.spriteCounter]
    sheepx = app.sheepx % 1000
    sheepy = app.sheepy
    canvas.create_image(sheepx, sheepy, image=ImageTk.PhotoImage(sprite))


def drawStart(app,canvas):
    canvas.create_image(500, 400, image=ImageTk.PhotoImage(app.startBg))
    drawSheep(app,canvas)
    canvas.create_text(800,20,text="Niubiest Sheep",fill="dodgerblue",
    font="Helvetica 30")
    canvas.create_text(800,50,text="Click Here To See Ranking",
    fill="dodgerblue", font="Helvetica 30")
    

def drawInstruction(app,canvas):
    canvas.create_image(500, 400, image=ImageTk.PhotoImage(app.bg))
    canvas.create_text(500,200,text="X+Y=Z",
    fill="red", font="Helvetica 45")
    canvas.create_text(500,300,text="boom!",
    fill="red", font="Helvetica 45")
    canvas.create_text(500,400,text="smart people understand",
    fill="red", font="Helvetica 50")
    canvas.create_text(500,620,text="CONTINUE",
    fill="dodgerblue", font="Helvetica 45")

def drawTopCards(app, canvas):
    for i in range(app.board.level-1, -1, -1):
        currLayer = app.board.cardList[i]
        for currCard in currLayer:
            if currCard.isTop:
                canvas.create_rectangle(currCard.upleftX, currCard.upleftY, 
                    currCard.upleftX+app.board.cardSize, currCard.upleftY+app.board.cardSize,
                    fill='wheat', outline='dodgerblue', width=3)
                canvas.create_image(currCard.upleftX+40, currCard.upleftY+40, image=ImageTk.PhotoImage(app.cardPics[currCard.num]))
                
def drawBotCards(app, canvas):
    for i in range(app.board.level-1, -1, -1):
        currLayer = app.board.cardList[i]
        for currCard in currLayer:
            if not currCard.isTop:
                canvas.create_rectangle(currCard.upleftX, currCard.upleftY, 
                    currCard.upleftX+app.board.cardSize, currCard.upleftY+app.board.cardSize,
                    fill='tan', outline='dodgerblue', width=3)
                canvas.create_image(currCard.upleftX+40, currCard.upleftY+40, image=ImageTk.PhotoImage(app.cardPicsUnder[currCard.num]))

def drawDeck(app, canvas):
    xpos = 200
    for i in range(7):
        c = app.board.cardDeck[i]
        if c == None:
            color = 'tan'
            canvas.create_rectangle(xpos+i*80, 650, xpos + i*80+80, 730,
                fill=color, outline='dodgerblue', width=3)
        else:
            canvas.create_image(xpos+i*80+40, 690,
                            image=ImageTk.PhotoImage(app.cardPics[c.num]))

def drawHand(app,canvas):
    if distance(app.finger1x,app.finger1y,app.finger2x,app.finger2y) < 40:
        canvas.create_oval(app.x-40,app.y-40,app.x+40,app.y+40,outline="mediumpurple",width=5)
    else:
        canvas.create_rectangle(app.x-40,app.y-40,app.x+40,app.y+40,outline="mediumpurple",width=5)
        

def drawRealGame(app,canvas):
    canvas.create_image(500, 400, image=ImageTk.PhotoImage(app.bg))
    canvas.create_text(100, 50,
            text = "Try openCV",
                fill="dodgerblue", font="Helvetica 28")
    drawBotCards(app, canvas)
    drawTopCards(app, canvas)
    drawDeck(app, canvas)
    if app.openCV:
        canvas.create_text(500, 10, text = "🖐️ to choose",
                fill="dodgerblue", font="Helvetica 15")
        canvas.create_text(500, 25, text = "🤏 to confirm",
                fill="dodgerblue", font="Helvetica 15")
        app.drawCamera(canvas) #draw app.frame on the canvas
        drawHand(app,canvas)
    

def drawRanking(app,canvas):
    canvas.create_rectangle(250, 200, 
                        750, 600,
                        fill='wheat', outline='dodgerblue', width=3)
    step = 50
    canvas.create_image(730, 250, image=ImageTk.PhotoImage(app.button))
    canvas.create_text(500, 260,
            text = "Ranking List",
                fill="dodgerblue", font="Helvetica 28")
    canvas.create_text(500, 300,
            text = "rank        name      score",
                fill="dodgerblue", font="Helvetica 28")
    for i in range(len(app.highScore)):
        playerName,playerScore = app.highScore[i]
        canvas.create_text(350, 
                340 + step * i,
                text = f'{i+1}',
                    fill = "dodgerblue", font = "Helvetica 28")
        canvas.create_text(500, 
                340 + step * i,
                text = f"{playerName}",
                    fill = "dodgerblue", font = "Helvetica 28")
        canvas.create_text(650, 
                340 + step * i,
                text = f"{playerScore}",
                    fill = "dodgerblue", font = "Helvetica 28")

def drawGameOver(app,canvas):
    canvas.create_image(500, 400, image=ImageTk.PhotoImage(app.bg))
    canvas.create_text(500,300,text= "GAME OVER",
    fill="white", font="Helvetica 50")
    canvas.create_text(500,400,fill="white", font="Helvetica 50",
    text= f"You score {app.score}!")
    canvas.create_text(500,500,fill="white", font="Helvetica 50",
    text= "HOME")


def redrawAll(app, canvas):
    if app.startGame == False:
        drawStart(app,canvas)
        if app.drawRanking:
            drawRanking(app,canvas)
    elif app.startGame: #already press start
        if app.instruction == False: 
            drawInstruction(app,canvas)
        elif app.instruction: #already display instruction
            drawRealGame(app,canvas)

    if app.isGameOver:
        drawGameOver(app,canvas)


runApp(width=1000, height=800)
   

    