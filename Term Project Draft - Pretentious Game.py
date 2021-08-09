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




lvl0: homeScreen
lvl1: establish controls 
lvl2 - 4: introduce obstacles, fire and enemies?
lvl5: backwards or random controls  (fire/eniems still in rest of these lvls)
lvl6: 
lvl7: world zoomed in
lvl8: ground disappering - either turning invisble, or falling off screen
lvl9: level changing every few seconds
lvl10: walk thorugh fire
lvl11: walk through eneimes
lvl12: end 
lvl13: back to homescreen
'''
'''
lvl0: 
    homescreen-- 
    have buttons to press - start
    if extra time: lvl selection in homescreen
lvl1: have keypressed buttons 
lvl2 - 4: have intersection reset block at beginnning of lvl, do damage????
lvl5: change controls, (changinf every few sec)???
lvl6: change player color to background color
lvl7: 
    change size of world and block (design at normal size then big up)
    make camera follow player
lvl8:
    if invisble: change ground to white on timer
    if falling: have ground move down every few seconds starting from L to R
lvl9: have block standing on not change, but rest of lvl change randomly 
lvl10: remove fire intersection rule
lvl11: remove enime and fire intersection rule
lvl12: go through lvl
lvl13: go back to home screen-- lvl 0
'''
'''
plan:
Classes: to stay organized
    -Player
    -Enemies (if included)
    -----?? less sure ??-----
    -Levels???
    -Platforms
'''

from cmu_112_graphics import *
import random
import time

class Player(object): #init//gravity//control//update
    #class for player

    def __init__(self, radius = 25, spawn = (100,340),color = 'crimson'):
        self.moveX = 0                      #change in horizontal movement 
        self.moveY = 0                      #change in vertical movement 
        self.radius = radius                #size
        self.spawnX, self.spawnY = spawn    #spawn pos
        self.posX = self.spawnX             #current X pos
        self.posY = self.spawnY             #current Y pos
        self.color = color
    
    def gravity(self,app):      #constantly moving player down//call every second
        self.moveY += 6.4       

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
                                fill = self.color)
    
    def jump(self,other):
        for i in range(len(other)):
            if self.posY == other[i].posY - other[i].height - self.radius:
                return True
            else:
                return False

class Platform(object): 
    def __init__(self,app,color = 'black'):
        self.posX = random.randint(0,app.width)
        self.posY = random.randint(0,app.height)
        self.width = random.randint(50,200)
        self.height = 20
        self.color = color

    def draw(self,canvas):
        canvas.create_rectangle(self.posX - self.width, self.posY - self.height, 
                                self.posX + self.width, self.posY + self.height, fill = self.color)

    def collides(self,other):       # STRUGGLE
        #true if x and y in platform
        # #contain bounds check
        if isinstance(other,Player):
        #if other is ball
            #problem ---------# w/checking if from top
            if self.posX - self.width < other.posX < self.posX + self.width and other.posY < self.posY: 
                if distance(0, self.posY, 0, other.posY) <= other.radius + self.height:
                    return True

            if self.posY - self.height < other.posY < self.posY + self.height and other.posX < self.posX:
                if distance(self.posX, 0, other.posX, 0) <= other.radius + self.width:
                    return True

        #check out --------------------------------------------------------------------------------------------------- HELP

        return False

    def update(self,app):           #updates player pos//call every second
        self.posX -= app.score

class NewPlatform(Platform):
    def __init__(self,app,color = 'black'):
        self.posX = app.width
        self.posY = random.randint(0,app.height)
        self.width = random.randint(50,200)
        self.height = 20
        self.color = color
    

def appStarted(app):
    app.topScore = 0
    app.score = 0
    app.time = 0

    app.player = Player()
    app.platforms = []
    for i in range(random.randint(5,7)):    #how make sure spawn a distance away
        app.platforms.append(Platform(app)) 
    app.gravityOn = True

def keyPressed(app,event):
    key = event.key

    if key == 'Up' or key == 'Space' or key == 'w' and app.player.jump(app.platforms): #fix//make so can only use on ground
        app.player.moveY = 0
        app.player.control(0, -50)
    
    if key == 'Right' or key == 'd':
        app.player.moveX = 0
        app.player.control(10, 0)
    
    if key == 'Left' or key == 'a':
        app.player.moveX = 0
        app.player.control(-10, 0)

def timerFired(app):
    app.time += 100
    app.score = app.time//1000

    platformUpdates(app)
    app.player.update()

    if app.gravityOn:
        app.player.gravity(app)
    
    if app.score > app.topScore:
        app.topScore = app.score
    
    

def platformUpdates(app):
    i = 0
    while i in range(len(app.platforms)):

        platform = app.platforms[i]
        if platform.collides(app.player):     #collison

            #FIX----------------------
            if platform.posX - platform.width < app.player.posX < platform.posX + platform.width and app.player.posY < platform.posY:
                app.player.posY = platform.posY - platform.height - app.player.radius # vertical collison

            elif platform.posY - platform.height < app.player.posY < platform.posY + platform.height and app.player.posX < platform.posX:
                app.player.posX = platform.posX - platform.width - app.player.radius
            #------------------------------

            app.player.moveX = 0
            app.player.moveY = 0
            app.gravityOn = False
        else:
            app.gravityOn = True
        
        platform.update(app)    #updates position of platform
    
        if platform.posX + platform.width < 0 and platform.posX < 0:    #new platforms
            app.platforms.pop(i)
            app.platforms.append(NewPlatform(app))
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
    drawPlatforms(app,canvas)
    drawPlayer(app,canvas)
    drawScore(app,canvas)
    
def drawPlatforms(app,canvas):
    for i in range(len(app.platforms)):
        app.platforms[i].draw(canvas)

def drawPlayer(app,canvas): 
    app.player.draw(canvas)

def drawScore(app,canvas):
    canvas.create_text(app.width*(2/3), 20, text = f'Score: {app.score}', font = 'Helvetica 20 bold', fill = 'crimson')

    canvas.create_text(app.width/3, 20, text = f'Top Score: {app.topScore}', font = 'Helvetica 20 bold', fill = 'crimson')


runApp(width = 1000, height = 900)