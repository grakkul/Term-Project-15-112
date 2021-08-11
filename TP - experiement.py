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

class Player(object): #init//gravity//control//update//draw
    #class for player
    def __init__(self, radius = 25, spawn = (480,420),color = 'aquamarine'):
        self.moveX = 0                      #change in horizontal movement 
        self.moveY = 0                      #change in vertical movement 

        self.radius = radius                #size
        self.spawnX, self.spawnY = spawn    #spawn pos
        self.posX = self.spawnX             #current X pos
        self.posY = self.spawnY             #current Y pos

        self.invincible = False
        self.color = color
    
    def gravity(self,app):      #constantly moving player down//call every second
        self.moveY += 6.4  
     
        if (self.posY) > app.height or (self.posY) < 0 or (self.posX) > app.width or (self.posX) < 0:  #if player goes off screen
            self.moveY = 0
            self.moveX = 0
            self.posY = self.spawnY
            self.posX = self.spawnX
            app.lifes -= 1
    
    def control(self,x,y):      #changes player movement//call in key pressed
        self.moveX += x
        self.moveY += y

    def update(self):           #updates player pos//call every second
        self.posX += self.moveX
        self.posY += self.moveY

    def draw(self,canvas):      #draw player
        canvas.create_oval(self.posX - self.radius, self.posY - self.radius, 
                                self.posX + self.radius, self.posY + self.radius,
                                fill = self.color, outline = self.color)

class Platform(object): #init//draw//collision//update//move
    def __init__(self,app,color = 'black'):
        self.width = random.randint(50,200)
        self.height = 15
        self.color = color
        self.direction = random.choice([-1,1])

        self.choiceDirection = random.randint(0,1)
        self.choiceMove = random.randint(0,1)

        self.spawnX = random.randint(app.width - 100,app.width + 50)  
        self.spawnY = random.randint(100,app.height - self.height)

        self.posX = self.spawnX
        self.posY = self.spawnY
        
    def draw(self,canvas):
        if self.choiceDirection == 0:
            canvas.create_rectangle(self.posX - self.width, self.posY - self.height, 
                                    self.posX + self.width, self.posY + self.height, fill = self.color, outline = self.color)
        else:                   
            canvas.create_rectangle(self.posY - self.height, self.posX - self.width, 
                                    self.posY + self.height, self.posX + self.width, fill = self.color, outline = self.color) 
                                                        
        # sideways = canvas.create_polygon()

    def checkPointCollison(self,x,y):
        if self.choiceDirection == 0:
            return (self.posX - self.width < x < self.posX + self.width and self.posY - self.height <  y < self.posY + self.height)
        else:
            return (self.posY - self.height < x < self.posY + self.height and self.posX - self.width <  y < self.posX + self.width)
      
    def collides(self,other):       
        if self.checkPointCollison(other.posX - other.radius,other.posY - other.radius):
            return True
        elif self.checkPointCollison(other.posX - other.radius,other.posY + other.radius):
            return True
        elif self.checkPointCollison(other.posX + other.radius,other.posY + other.radius):
            return True
        elif self.checkPointCollison(other.posX + other.radius,other.posY - other.radius):
            return True
        else:
            return False

    def update(self,app):           #updates player pos//call every second
        self.posX -= (20 + (app.time/1000)*.5)

    def move(self):                 #moves platforms up and down
        if self.choiceMove == 0:
            self.color = 'slate blue'
            range = self.height * 3

            if self.posY <= self.spawnY - range: 
                self.direction = 1
            elif self.posY >= self.spawnY + range:
                self.direction = -1
        
            self.posY += (5 * self.direction)
        else:
            self.posY = self.posY

class NewPlatform(Platform):
    def __init__(self,app):
        super().__init__(app)
        if self.choiceDirection == 0:
            self.spawnY = random.randint(int(app.player.posY - app.sdRowsBounds[1]), int(app.player.posY + app.sdRowsBounds[3]))
        else:
            self.spawnX = random.randint(int(app.player.posY - app.sdColsBounds[0]), int(app.player.posY + app.sdColsBounds[2]))


def appStarted(app):
    app.topScore = 0
    app.backColor = ['white','SpringGreen','DeepSkyBlue','MediumPurple','DeepPink','crimson']
    reset(app)

def reset(app): #what gets called when reset game
    app.gameOver = False
    app.score = 0
    app.time = 0
    app.seconds = 0
    app.lifes = 3
    app.invincibleTime = 0
    
    app.player = Player()
    app.platforms = []
    for i in range(random.randint(5,9)):    #how make sure spawn a distance away
        app.platforms.append(Platform(app)) 
    
    userAnalysis(app)
   
def userAnalysis(app): 
    app.rows = app.height // (app.player.radius*4) # == 9
    app.cols = app.width // (app.player.radius*4) # == 10

    app.sdRows = 0 #standard deviation rows
    app.sdRowsBounds = 0
    app.sdCols= 0  #standard deviation cols
    app.sdColsBounds = 0

    app.twoDL = []
    app.sumRow = []
    app.sumCol = []
    app.sumTotal = 0

    for row in range(app.rows):
        app.twoDL += [[0]*app.cols]
        app.sumRow.append(0)

    for col in range(app.cols):
        app.sumCol.append(0)

def keyPressed(app,event): #player movement
    key = event.key

    if key == 'r':
        reset(app)

    if app.gameOver:
        return

    if key == 'Up' or key == 'Space' or key == 'w':
        app.player.moveY = 0
        app.player.control(0, -30)
    
    if key == 'Right' or key == 'd':
        app.player.moveX = 0
        app.player.control(10, 0)
    
    if key == 'Left' or key == 'a':
        app.player.moveX = 0
        app.player.control(-10, 0)

def timerFired(app): #do downgrades
    if app.gameOver:
        return

    app.time += 100
    app.score = app.time//1000

    if time.time() > app.invincibleTime + 3:
        app.player.invincible = False

    platformUpdates(app)
    app.player.update()
    app.player.gravity(app)

    if app.lifes <= 0:
        app.gameOver = True

    if app.score > app.topScore:
        app.topScore = app.score

    #if done with MVP do downgrades
        #DOWNGRADES CALLING -------------
        # print(app.time % 10000000000) 
        # if app.time % 10000000000:  #TROUBLE
        #     lvl = random.randint(0,2)
        #     # downgrades(app,lvl)
        #-----------------------------------

    #find ball locastion, add 1 for every 10ms
    playerRow, playerCol = getCell(app, app.player.posX, app.player.posY)
    app.twoDL[playerRow][playerCol] += 1

    #make 1D lists for sumRow and sumCol and sumTotal
    sumLists(app)

    print('row',app.sumRow)
    print('col',app.sumCol)
    print('total',app.sumTotal)

    app.sdRows = standardDeviation(app.sumRow)
    app.sdRowsBounds = getCellBounds(app, app.sdRows, 0)
    app.sdCols = standardDeviation(app.sumCol)
    app.sdColsBounds = getCellBounds(app, 0, app.sdCols)

    print(app.sdRows,app.sdCols)

    # sdRowsc = standardDeviation(app.sumCol) 
    
    # print(sdRowsc)

    #-IN DEVELOPMENT------------------------------------------------------------- \/
    #use sums to get proabablity

    # num = random.randint(0,100)
    # if num is in sumCol[i]/sumTotal spawn in that col(for vert)
    # if num is in sumRow[i]/sumTotal spawn in that row(for horz)

    # get col and row of highest num???
    
    # then use probaility to inglucence platform generation
    # use randome.triange(lo,hi,mode) or standard deviation????
    #-----------------------------------------------------------------\/
    # how to use derivation to influence spawn location???????????
        #have spawn closer to hump?? how
     

def sumLists(app): #1d list of Rows and Cols//int of total Sum
    for row in range(app.rows):
        app.sumRow[row] = 0
        for col in range(app.cols):
            app.sumRow[row] += app.twoDL[row][col]  

    for col in range(app.cols):
        app.sumCol[col] = 0
        for row in range(app.rows):
            app.sumCol[col] += app.twoDL[row][col]             
    
    app.sumTotal = sumTotal(app)

def sumTotal(app): #total sum
        total = 0
        for row in range(app.rows):
            for col in range(app.cols):
                num = app.twoDL[row][col]
                total += num
        return total
    
def downgrades(app,lvl): #do when MVP acheived
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

def platformUpdates(app): 
    i = 0
    while i in range(len(app.platforms)):
        platform = app.platforms[i]

        platform.update(app)    #updates position of platform
        platform.move()         #make every few move
    
        if app.player.invincible == False:  #color switch for invisible    
            app.player.color = 'aquamarine'
        else:
            app.player.color = 'DodgerBlue2'

        if platform.collides(app.player):     #collison - keeps taking too much damgae 
            if app.player.invincible == False:
                app.lifes -= 1

            app.player.invincible = True
            app.invincibleTime = time.time()

        if platform.posX + platform.width < 0:  #summons new platforms and pops old ones
            app.platforms.append(NewPlatform(app)) 
            app.platforms.pop(i)
        else:
            i += 1

def distance(x0,y0,x1,y1):
	return ((x1-x0)**2 + (y1-y0)**2)**.5

def checkPlatformIsLegal(self,app): #NOT FINFINISHED
    return
            # if self.posX - self.width < other.posX < self.posX + self.width:
            #     if distance(0, self.posY, 0, other.posY) <= 2*self.width:
            #         return True

            # if self.posY - self.height < other.posY < self.posY + self.height:
            #     if distance(self.posX, 0, other.posX, 0) <= 3*self.height:
            #         return True

#citation: derived from sdRows formula
def standardDeviation(L): #standard deviation forumla
    total=0
    for i in range(len(L)):
        #sdRows = ((sum of((x[i]-avg)**2))/ len(x)-1)**.5
        total += i * L[i]
    avg = total/sum(L)
    numerator = 0

    for i in range(len(L)):
        numerator += (L[i] - avg)**2
        
    sdRows = ((numerator)/sum(L))**0.5
    return sdRows

def redrawAll(app,canvas):
    if app.gameOver:
        drawGameOver(app,canvas)
    else:
        drawBackground(app,canvas)
        drawPlatforms(app,canvas)
        drawPlayer(app,canvas)
        drawScore(app,canvas)
        drawGrid(app,canvas)
    
def drawBackground(app,canvas):  # how to filter through???
    # i = 0
    # while i in range(len(app.backColor)):
    #     if app.score % 10:
    #         i += 1
    #     canvas.create_rectangle(0,0,app.width,app.height, fill = app.backColor[i])
   
    canvas.create_rectangle(0,0,app.width,app.height, fill = app.backColor[0])

def drawPlatforms(app,canvas):
    for i in range(len(app.platforms)):
        app.platforms[i].draw(canvas)

def drawPlayer(app,canvas): 
    app.player.draw(canvas)
    
def drawScore(app,canvas):
    canvas.create_text(app.width/2, 20, text = f'Score: {app.score}', font = 'Helvetica 20 bold', fill = 'crimson')

    canvas.create_text(app.width*(.8), 20, text = f'Top Score: {app.topScore}', font = 'Helvetica 20 bold', fill = 'crimson', anchor = 'w')
    canvas.create_text(20, 20, text = f'Lifes: {app.lifes}', font = 'Helvetica 20 bold', fill = 'crimson', anchor = 'w')

def drawGameOver(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'black')
    canvas.create_text(app.width/2,100, text = f'GAME OVER', fill = 'crimson', font = 'Helvetica 46 bold')
    canvas.create_text(app.width/2,app.height/2 - 40, text = f'Best Score: {app.topScore}', fill = 'crimson', font = 'Helvetica 20 bold')
    canvas.create_text(app.width/2,app.height/2, text = f'Final Score: {app.score}', fill = 'crimson', font = 'Helvetica 20 bold')
    canvas.create_text(app.width/2,app.height/2 + 100, text = "Press 'r' to Reset", fill = 'crimson', font = 'Helvetica 20 bold')

#citation: taken from my hw5
def getCell(app, x, y):
    gridWidth  = app.width
    gridHeight = app.height 
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y) / cellHeight)
    col = int((x) / cellWidth)
    return (row, col)

#citation: taken from my hw9: tetris
def getCellBounds(app, row, col):
    gridWidth  = app.width 
    gridHeight = app.height 
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    x0 =  col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight

    return (x0, y0, x1, y1)

def drawGrid(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0,y0,x1,y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0,y0,x1,y1)
            canvas.create_text(x0 + app.player.radius, y0 + app.player.radius, text = app.twoDL[row][col])

runApp(width = 1000, height = 900)