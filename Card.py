import random

class Card():
    def __init__(self, layer):
        self.upleftX = random.randrange(180, 740, 20)
        self.upleftY = random.randrange(150, 550, 20)
        self.num = random.randint(1, 9)
        self.layer = layer
        if (layer == 0): 
            self.isTop = True
        else: 
            self.isTop = False
        
    def overlap(self, c):
        # if self.layer != c.layer:
        #     return False
        
        return ((c.upleftX >= self.upleftX and c.upleftX <= self.upleftX+80
            and c.upleftY >= self.upleftY and c.upleftY <= self.upleftY+80)
            or (c.upleftX+80 >= self.upleftX and c.upleftX+80 <= self.upleftX+80
            and c.upleftY >= self.upleftY and c.upleftY <= self.upleftY+80)
            or (c.upleftX >= self.upleftX and c.upleftX <= self.upleftX+80
            and c.upleftY+80 >= self.upleftY and c.upleftY+80 <= self.upleftY+80)
            or (c.upleftX+80 >= self.upleftX and c.upleftX+80 <= self.upleftX+80
            and c.upleftY+80 >= self.upleftY and c.upleftY+80 <= self.upleftY+80))
    
    def overlap2(self, c):
        return ((c.upleftX > self.upleftX and c.upleftX < self.upleftX+80
            and c.upleftY > self.upleftY and c.upleftY < self.upleftY+80)
            or (c.upleftX+80 > self.upleftX and c.upleftX+80 < self.upleftX+80
            and c.upleftY > self.upleftY and c.upleftY < self.upleftY+80)
            or (c.upleftX > self.upleftX and c.upleftX < self.upleftX+80
            and c.upleftY+80 > self.upleftY and c.upleftY+80 < self.upleftY+80)
            or (c.upleftX+80 > self.upleftX and c.upleftX+80 < self.upleftX+80
            and c.upleftY+80 > self.upleftY and c.upleftY+80 < self.upleftY+80))
