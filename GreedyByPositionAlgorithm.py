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
# CLASS: GreedyByPositionAlgorithm
#
# Members: 		name of algorithm, team
#						
# Functions:	addNextPlayer - Decides which Player should be drafted next by this algorithm
#						args:		
#						returns:	Name of player
#
##########################################################################################

class GreedyByPositionAlgorithm(Algorithm):

	def __init__(self):
		self.name = ""
		self.team = Team()
		self.filledPositions = []
		self.maxedPositions = []

	def __init__(self, inputName):
		self.name = str(inputName)
		self.team = Team()
		self.filledPositions = []
		self.maxedPositions = []

	def checkFilledPositions(self):
		if "QB" not in self.filledPositions and len(self.team.QBs) >= STARTING_QBS:
			self.filledPositions.append("QB")
		if "RB" not in self.filledPositions and len(self.team.RBs) >= STARTING_RBS:
			self.filledPositions.append("RB")
		if "WR" not in self.filledPositions and len(self.team.WRs) >= STARTING_WRS:
			self.filledPositions.append("WR")
		if "TE" not in self.filledPositions and len(self.team.TEs) >= STARTING_TES:
			self.filledPositions.append("TE")
		if "PK" not in self.filledPositions and len(self.team.PKs) >= STARTING_KS:
			self.filledPositions.append("PK")

	def chooseNextPlayer(self, year):
		sqlHandler = SQL_HANDLER()
		print len(self.filledPositions)
		if len(self.filledPositions) != 0 and len(self.filledPositions) < 5:
			positionString = ""
			i = 1
			for position in self.filledPositions:
				print position
				print len(self.filledPositions)
				if i == 1:
					positionString = "\'" + position + "\'"
				else:
					positionString = positionString + " AND Pos!=" + "\'" + position + "\'"
				i = i + 1
				data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' AND Pos!=" + positionString + " ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
		else:
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
		return data

	def addNextPlayer(self, year):	
		data = self.chooseNextPlayer(year)
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.team.addPlayer(newPlayer)
		self.updateList(year, newPlayer)