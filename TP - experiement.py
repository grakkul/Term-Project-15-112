'''
infinate side scroller
    - diffrent challenges as power ups
        -you are invisible  - turn your color white for a bit
        -ground disappering - background turns black for a bit every half second
    - power up that makes scrolling speed back to original
        -self.posX = app.score/2
    - side scrolling speeds up as time goes on
    - score = time since start
    - keep memory of score
    - if go off screen or fall off map you lose
'''

from cmu_112_graphics import *
import random
import time

class Player(object): #init//gravity//control//update
    #class for player

    def __init__(self, radius = 25, spawn = (100,340),color = 'aquamarine'):
        self.moveX = 0                      #change in horizontal movement 
        self.moveY = 0                      #change in vertical movement 
        self.radius = radius                #size
        self.spawnX, self.spawnY = spawn    #spawn pos
        self.posX = self.spawnX             #current X pos
        self.posY = self.spawnY             #current Y pos
        self.color = color
    
    def gravity(self,app):      #constantly moving player down//call every second
        self.moveY += 6.4  

        #MOVE TO GAME OVER??     
        if (self.posY) > app.height or (self.posX) > app.width or (self.posX) < 0:  #if player goes off screen
            self.moveY = 0
            self.moveX = 0
            self.posY = self.spawnY
            self.posX = self.spawnX
    
    def control(self,x,y):      #changes player movement//call in key pressed
        self.moveX += x
        self.moveY += y

    def update(self):           #updates player pos//call every second
        self.posX += self.moveX
        self.posY += self.moveY

    def draw(self,canvas):      #draw player
        canvas.create_rectangle(self.posX - self.radius, self.posY - self.radius, 
                                self.posX + self.radius, self.posY + self.radius,
                                fill = self.color, outline = self.color)
    
    # def jump(self,other):
    #     for i in range(len(other)):
    #         if self.posY == other[i].posY - other[i].height - self.radius:
    #             return True
    #         else:
    #             return False

class Platform(object): #problems
    def __init__(self,app,color = 'black'):
        self.width = random.randint(50,200)
        self.height = 15
        self.color = color
        self.choice = random.randint(0,1)
        self.direction = random.choice([-1,1])

        self.spawnX = random.randint(app.width - 100,app.width + 50)
        self.spawnY = random.randint(100,app.height - self.height)
        self.posX = self.spawnX
        self.posY = self.spawnY
        

    def draw(self,canvas):
        if self.choice == 0:
            canvas.create_rectangle(self.posX - self.width, self.posY - self.height, 
                                            self.posX + self.width, self.posY + self.height, fill = self.color)
        else:                   
            canvas.create_rectangle(self.posY - self.height,self.posX - self.width, 
                                            self.posY + self.height, self.posX + self.width, fill = self.color)  
        # sideways = canvas.create_polygon()
              
    def collides(self,other):       # STRUGGLE
        if isinstance(other,Player):
        #if other is ball
            #problem ---------# w/checking if from top
            if self.posX - self.width < other.posX < self.posX + self.width and other.posY < self.posY: 
                # if distance(0, self.posY, 0, other.posY) <= other.radius + self.height:
                if abs(self.posY - other.posY) <= other.radius + self.height:
                    return True

            if self.posY - self.height < other.posY < self.posY + self.height and other.posX < self.posX:
                # if distance(self.posX, 0, other.posX, 0) <= other.radius + self.width:
                if abs(self.posX - other.posX) <= other.radius + self.width:
                    return True
        return False

    def update(self,app):           #updates player pos//call every second
        self.posX -= (20 + (app.time/1000)*.5) #app.time/100

    def move(self,app):
        if self.choice == 0:
            range = self.height * 3

            if self.posY <= self.spawnY - range: 
                self.direction = 1
            elif self.posY >= self.spawnY + range:
                self.direction = -1
        
            self.posY += (5 * self.direction)
        else:
            self.posY = self.posY

def appStarted(app):
    app.topScore = 0
    app.score = 0
    app.time = 0
    app.counter = 0
    # app.backColor = 'white'
    app.backColor = ['white','SpringGreen','DeepSkyBlue','MediumPurple','DeepPink','crimson']
    app.lifes = 3
    

    app.player = Player()
    app.platforms = []
    for i in range(random.randint(5,8)):    #how make sure spawn a distance away
        app.platforms.append(Platform(app)) 

def keyPressed(app,event):
    key = event.key

    if key == 'Up' or key == 'Space' or key == 'w':
        app.player.moveY = 0
        app.player.control(0, -30)
    
    if key == 'Right' or key == 'd':
        app.player.moveX = 0
        app.player.control(10, 0)
    
    if key == 'Left' or key == 'a':
        app.player.moveX = 0
        app.player.control(-10, 0)

def timerFired(app): #Problems
    app.time += 100
    app.score = app.time//1000
    app.counter += 1//10    #seconds

    platformUpdates(app)
    app.player.update()
    app.player.gravity(app)

    # print(app.time % 10000000000)

    # if app.time % 10000000000:  #TROUBLE
    #     lvl = random.randint(0,2)
    #     # downgrades(app,lvl)

    if app.score > app.topScore:
        app.topScore = app.score

def downgrades(app,lvl):
    if lvl == 0:
        return

    elif lvl == 1:
        app.backColor = app.player.color 
        if app.score % 3:
            app.backColor = 'white'
    
    elif lvl == 2:
        for i in range(len(app.platforms)):
            platform = app.platforms[i]
            app.backColor = platform.color 
            if app.score % 3:
                app.backColor = 'white'

def platformUpdates(app): #Problems
    i = 0
    while i in range(len(app.platforms)):

        platform = app.platforms[i]
        if platform.collides(app.player):     #collison - keeps taking too much damgae 
            #restart
            app.lifes -= 1
            if app.lifes == 0:
                appStarted(app)
        
        platform.update(app)    #updates position of platform

        #make every few move --> for m in range(len(app.platforms),2): 
        #how make come back down
        platform.move(app)
    
        # if platform.posX + platform.width < app.width/2:    #new platforms
        #     app.platforms.append(Platform(app)) #how to not summon an army

        if platform.posX + platform.width < 0:
            app.platforms.append(Platform(app)) 
            app.platforms.pop(i)
        else:
            i += 1

def distance(x0,y0,x1,y1):
	return ((x1-x0)**2 + (y1-y0)**2)**.5

def checkPlatformIsLegal(self,app):
    return
            # if self.posX - self.width < other.posX < self.posX + self.width:
            #     if distance(0, self.posY, 0, other.posY) <= 2*self.width:
            #         return True

            # if self.posY - self.height < other.posY < self.posY + self.height:
            #     if distance(self.posX, 0, other.posX, 0) <= 3*self.height:
            #         return True

def redrawAll(app,canvas):
    drawBackground(app,canvas)
    drawPlatforms(app,canvas)
    drawPlayer(app,canvas)
    drawScore(app,canvas)
    
def drawBackground(app,canvas):
    # i = 0
    # while i in range(len(app.backColor)):
    #     canvas.create_rectangle(0,0,app.width,app.height, fill = app.backColor[i])
    i = 0
    if app.counter % 10:
        i += 1
    canvas.create_rectangle(0,0,app.width,app.height, fill = app.backColor[i])

def drawPlatforms(app,canvas):
    for i in range(len(app.platforms)):
        app.platforms[i].draw(canvas)


def drawPlayer(app,canvas): 
    app.player.draw(canvas)
    

def drawScore(app,canvas):
    canvas.create_text(app.width*(2/3), 20, text = f'Score: {app.score}', font = 'Helvetica 20 bold', fill = 'crimson')

    canvas.create_text(app.width/3, 20, text = f'Top Score: {app.topScore}', font = 'Helvetica 20 bold', fill = 'crimson')
    canvas.create_text(20, 20, text = f'lifes: {app.lifes}', font = 'Helvetica 20 bold', fill = 'crimson', anchor = 'w')


runApp(width = 1000, height = 900)