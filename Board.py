from curses import flash
from Card import *

class Board():
    def __init__(self, level, cardSize):
        self.empty = True
        self.level = level
        self.cardList = [[] for i in range(self.level)]
        self.cardSize = cardSize
        self.cardDeck = [None, None, None, None, None, None, None]
        self.deckPos = 0
        self.maxCard = 25
    
    

    def fillBoard(self):
        for i in range(self.level-1, -1, -1):
            for j in range(100):
                add = True
                card = Card(i)
                for compareCard in self.cardList[i]:
                    if card.overlap(compareCard):
                        add = False
                        # break
                if add:
                    self.cardList[i].append(card)

    # def fillBoard(self):
    #     for l in range(self.level):
    #         count = 0
    #         fill = [[0] * (640 / 20) for f in range(480 / 2)]
    #         while count < self.maxCard:
    #             newC = Card(l)
    #             posX = newC.upleftX / 20
    #             posY = newC.upleftY / 20
    #             for i in range(4):
    #                 for j in range(4):
    #                     if fill[i+posX][j+posY] == 1:
    #                         continue
    #                     fill[i+posX][j+posY] = 1
    #             count += 1

    def win(self):
        for i in range(self.level):
            if len(self.cardList[i]) != 0:
                return False
        return True

    def updateDeck(self, app, new):
        new = app.chosenCard
        d = {}
        for i in range(7):
            currCard = self.cardDeck[i]
            for j in range(i, 7):
                compareCard = self.cardDeck[j]
                if currCard != None and compareCard != None:
                    diff = abs(currCard.num - compareCard.num)
                    total = currCard.num + compareCard.num
                    d[diff] = (i, j)
                    d[total] = (i, j)
        if new.num in d:
            (first, second) = d[new.num]
            if (first <= second):
                self.cardDeck.pop(first)
                self.cardDeck.pop(second-1)
            else:
                self.cardDeck.pop(second)
                self.cardDeck.pop(first-1)
            self.deckPos -= 2
            self.cardDeck.append(None)
            self.cardDeck.append(None)
            updated = []
            for c in self.cardDeck:
                if c != None:
                    updated.append(c)
            for i in range(7 - self.deckPos):
                updated.append(None)
            # self.cardDeck = updated
        
        else:
            self.cardDeck[self.deckPos] = new
            self.deckPos += 1
            if self.deckPos == 6: 
                app.gameOver = True
    
    def removeCard(self, x, y):
        for i in range(self.level):
            currLayer = self.cardList[i]
            for j in range(len(currLayer)):
                if (currLayer[j].upleft.X <= x and x <= currLayer[j].upleft.X+self.cardSize
                    and currLayer[j].upleft.Y <= y and x <= currLayer[j].upleft.Y+self.cardSize):
                    currLayer.pop(j)

    def updateTop(self):
        for i in range(self.level):
            currLayer = self.cardList[i]
            for currCard in currLayer:
                if currCard.isTop: break
                for j in range(i):
                    compareList = self.cardList[j]
                    for compareCard in compareList:
                        if currCard.overlap(compareCard):
                            continue
                currCard.isTop = True
