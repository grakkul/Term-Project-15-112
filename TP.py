
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

class NewPlatform(Platform): #init//spawn
    def __init__(self,app):
        super().__init__(app)

        totalR=0
        for i in range(len(app.sumRow)):
            totalR += i * app.sumRow[i]
        avgR = totalR/sum(app.sumRow)

        totalC=0
        for i in range(len(app.sumCol)):
            totalC += i * app.sumCol[i]
        avgC = totalC/sum(app.sumCol)

        while True:
            numRow = random.gauss(avgR, app.sdRows)
            numCol = random.gauss(avgC, app.sdCols)
            if 0 <= numRow < app.rows and 0 <= numCol <= app.cols:
                break

        x0,y0,x1,y1 = getCellBounds(app, numRow, numCol)

        if self.choiceDirection == 0:  
            self.spawnY = random.randint(int(y0), int(y1))
            self.spawnX = random.randint(app.width - 100,app.width + 50) 
            self.posX = self.spawnX
            self.posY = self.spawnY

            app.temp.append(self.spawnY) #check this is correct---------------------------------------------------------------------
           
            print(app.temp)
        else:
            self.spawnY = random.randint(int(x0), int(x1))
            self.spawnX = random.randint(app.width - 100,app.width + 50) 
            self.posX = self.spawnX
            self.posY = self.spawnY

class Bonus(object): #init//draw//collison
    def __init__(self, app):
        self.posX = random.randint(50, app.width - 50)
        self.posY = random.randint(50, app.height - 50)
        self.radius = 15
        self.color = 'white'

    def draw(self,canvas):
        canvas.create_oval(self.posX - self.radius, self.posY - self.radius, 
                           self.posX + self.radius, self.posY + self.radius,
                           fill = self.color, outline = self.color)

    def collision(self, other):
        if distance(self.posX,self.posY,other.posX,other.posY) <= self.radius + other.radius:
            return True
        else:
            return False

def appStarted(app):
    app.started =False
    app.topScore = 0
    reset(app)

def reset(app): #what gets called when reset game
    app.gameOver = False
    app.score = 0
    app.bonusScore = 0

    app.time = 0
    app.seconds = 0

    app.lifes = 3
    app.invincibleTime = 0
    
    app.player = Player()
    app.bonus = Bonus(app)
    app.platforms = []
    for i in range(random.randint(5,9)):    #how make sure spawn a distance away
        app.platforms.append(Platform(app)) 
    
    userAnalysis(app)
   
def userAnalysis(app): #algorithmic complexity starter
    app.temp = []
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
    
    if key == 'h':
        reset(app)
        app.started = not app.started
       
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
    if app.started == False:
        return
    if app.gameOver:
        return

    app.time += 100
    app.score = app.time//1000 + app.bonusScore

    if time.time() > app.invincibleTime + 3:
        app.player.invincible = False

    platformUpdates(app)
    app.player.update()
    app.player.gravity(app)

    if app.bonus.collision(app.player): #checks for bonus collison
        app.bonusScore += 5
        app.bonus.posX = random.randint(50, app.width - 50)
        app.bonus.posY = random.randint(50, app.height - 50)

    if app.lifes <= 0: #checks to see if dead
        app.gameOver = True

    if app.score > app.topScore: #sets topScore
        app.topScore = app.score

    #find ball locastion, add 1 for every 10ms
    playerRow, playerCol = getCell(app, app.player.posX, app.player.posY)
    app.twoDL[playerRow][playerCol] += 1

    #make 1D lists for sumRow and sumCol and sumTotal
    sumLists(app)

    #find sd of rows and cols
    app.sdRows = standardDeviation(app.sumRow)
    app.sdCols = standardDeviation(app.sumCol)

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
    
def platformUpdates(app): # update//move//collision//spawn
    i = 0
    while i in range(len(app.platforms)):
        platform = app.platforms[i]

        platform.update(app)    #updates position of platform
        platform.move()         #make every few move
    
        if app.player.invincible == False:  #color switch for invisible    
            app.player.color = 'aquamarine'
        else:
            app.player.color = 'LightSteelBlue'

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
        
def distance(x0,y0,x1,y1): #helper fn
	return ((x1-x0)**2 + (y1-y0)**2)**.5

#citation: derived from standard deviation formula
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

#citation: taken from my hw5
def getCell(app, x, y): #helper fn
    gridWidth  = app.width
    gridHeight = app.height 
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y) / cellHeight)
    col = int((x) / cellWidth)
    return (row, col)

#citation: taken from my hw9: tetris
def getCellBounds(app, row, col): #helper fn
    gridWidth  = app.width 
    gridHeight = app.height 
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    x0 =  col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight

    return (x0, y0, x1, y1)

def redrawAll(app,canvas): #draws to canvas
    if app.started == False:
        drawStartScreen(app,canvas)
    elif app.gameOver:
        drawGameOver(app,canvas)
    else:
        drawBackground(app,canvas)
        drawGrid(app,canvas)
        drawPlatforms(app,canvas)
        drawBonus(app,canvas)
        drawPlayer(app,canvas)
        drawScore(app,canvas)
        
def drawBackground(app,canvas): 
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'LightSeaGreen')

def drawGrid(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0,y0,x1,y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0,y0,x1,y1, outline ="DarkCyan")

            #temporary -- to help build algortithmic method
            # canvas.create_text(x0 + app.player.radius, y0 + app.player.radius, text = app.twoDL[row][col])

def drawPlatforms(app,canvas):
    for i in range(len(app.platforms)):
        app.platforms[i].draw(canvas)

def drawPlayer(app,canvas): 
    app.player.draw(canvas)

def drawBonus(app,canvas):
    app.bonus.draw(canvas)

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
    canvas.create_text(app.width/2,app.height/2 + 150, text = "Press 'h' to go to HomeScreen", fill = 'crimson', font = 'Helvetica 20 bold')

def drawStartScreen(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'black')
    canvas.create_rectangle(100,50,app.width-100,app.height-100, fill = 'LightSeaGreen')
    canvas.create_text(app.width/2,100, text = f'RUNAWAY', fill = 'black', font = 'Helvetica 46 bold')
    canvas.create_rectangle(200, 150,app.width-200,160, fill = 'black')
    canvas.create_text(app.width/2,app.height/2 - 100, text = f"Press 'h' to Start :)", fill = 'black', font = 'Helvetica 16 bold')
    canvas.create_text(app.width/2,app.height/2 - 80, text = f"(or to come back here once you start)", fill = 'black', font = 'Helvetica 16 bold')
    canvas.create_text(app.width/2,app.height/2 - 20, text = f"Press 'r' to Restart", fill = 'black', font = 'Helvetica 16 bold')
    canvas.create_text(app.width/2,app.height/2 + 60, text = f"Use 'w,s,d' to move", fill = 'black', font = 'Helvetica 16 bold')
    canvas.create_text(app.width/2,app.height/2 + 80, text = f"(or use the arrow keys)", fill = 'black', font = 'Helvetica 16 bold')
    canvas.create_text(app.width/2,app.height - 200, text = f'Best Score: {app.topScore}', fill = 'black', font = 'Helvetica 20 bold')

runApp(width = 1000, height = 900)
