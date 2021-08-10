# Term-Project-15-112

Project Description [5 pts]: The name of the term project and a short description of what it will be.

Structural Plan [5 pts]: A structural plan for how the finalized project will be organized in different functions, files and/or objects.

Algorithmic Plan [5 pts]: 
A detailed algorithmic plan for how you will approach the trickiest part of the project. 
Be sure to clearly highlight which part(s) of your project are algorithmically most complex, 
and include details of the algorithm(s) you are using in those cases.

Version Control Plan [5 pts]: A short description and image demonstrating how you are using version control to back up your code. Notes:

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
	no enemies

algorithmic plan:
	
	user analysis:
		use 2D list to keep track of where player has been and use to spawn obstacles nearer to the player.
