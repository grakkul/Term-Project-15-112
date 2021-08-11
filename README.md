# Term-Project-15-112

TP 1
----
name: 
	Block Dash or Where Am I?

short description:	
	A 2D platformer, an inifinate lvl where your score is determined by how long you survive. 
	Downgrades will come randomly for a few seconds
	
structural plan:

	Classes:
		Player info
		Enemy info - if there is a enemy
		Platform info
		
	functions:
		appstarted - to establish class cases
		keypressed - for movement
		timerFired - for updating platform pos, and keeping consistant gravity
		redrawAll - draw: player, platforms
	
algorithmic plan:

	user analysis
		- how have they lost theri lives?
		- new lvl generation taylored to be harder

TP2 Update:
-----

description:
	A 2D avoid the obstacles game, an inifinate lvl where your score is determined by how long you survive. If you spend too much time in one place more platforms spawn to go there.
	
structural plan:
	
	Classes:
		player info - init//gravity//control//update//draw
		platform info - init//draw//collision//update//move
		newPlatform info - init 
	Functions:
		appStarted
		reset
		userAnalysis
		keypressed
		timerFired
		sumLists
		downgrades
		platformUpgrades
		distance
		standardDeviation
		getCell
		getCellBounds
		redrawAll
		drawBackground
		drawPlatforms
		drawPlayer
		drawScore
		drawGameOver
		drawGrid

algorithmic plan:
	
	user analysis:
		using a 2D list to keep track of where player has been
		create 1D list of sum row and col based on 2D list
		use 1D lists to find standard deviation
		use standard deviation to spawn platforms nearer to player
