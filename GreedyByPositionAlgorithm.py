import teamClass
from Algorithm import *
import sqlite3 as lite

# Maximum Number of players from each position allowed on a roster
MAX_QBS_PER_TEAM = 4
MAX_RBS_PER_TEAM = 8
MAX_WRS_PER_TEAM = 8
MAX_TES_PER_TEAM = 3
MAX_DSTS_PER_TEAM = 3
MAX_KS_PER_TEAM = 3

#STARTING TEAM (standard)
STARTING_QBS = 1
STARTING_RBS = 2
STARTING_WRS = 2
STARTING_TES = 1
STARTING_KS = 1
STARTING_DEFS = 1 
STARTING_FLEX = 1

TEAM_SIZE = 16

##########################################################################################
#
# CLASS: greedyByPositionAlgorithm
#
# Members: 		name of algorithm, team
#						
# Functions:	addNextPlayer - Decides which Player should be drafted next by this algorithm
#						args:		
#						returns:	Name of player
#
##########################################################################################

class greedyByPositionAlgorithm(Algorithm):

	def __init__(self):
		self.name = ""
		self.team = Team()
		self.filledPositions = []
		self.maxedPositions

	def __init__(self, inputName):
		self.name = str(inputName)
		self.team = Team()
		self.filledPositions = []

	def addNextPlayer(self, year):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.team.addPlayer(newPlayer)
		self.updateList(year, newPlayer)