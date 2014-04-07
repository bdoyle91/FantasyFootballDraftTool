import teamClass
from Algorithm import *
import sqlite3 as lite
from LeagueSettings import *


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
		self.year = -1
		self.filledPositions = []
		self.maxedPositions = []

	def __init__(self, inputName):
		self.name = str(inputName)
		self.team = Team()
		self.year = -1
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
		if "D/ST" not in self.filledPositions and len(self.team.DEFs) >= STARTING_DEFS:
			self.filledPositions.append("D/ST")

	def checkMaxedPositions(self):
		if "QB" not in self.maxedPositions and len(self.team.QBs) >= MAX_QBS:
			self.maxedPositions.append("QB")
		if "RB" not in self.maxedPositions and len(self.team.RBs) >= MAX_RBS:
			self.maxedPositions.append("RB")
		if "WR" not in self.maxedPositions and len(self.team.WRs) >= MAX_WRS:
			self.maxedPositions.append("WR")
		if "TE" not in self.maxedPositions and len(self.team.TEs) >= MAX_TES:
			self.maxedPositions.append("TE")
		if "PK" not in self.maxedPositions and len(self.team.PKs) >= MAX_KS:
			self.maxedPositions.append("PK")
		if "D/ST" not in self.maxedPositions and len(self.team.DEFs) >= MAX_DSTS:
			self.maxedPositions.append("D/ST")

	def generateStarterDraftString(self):
		positionString = ""
		i = 1
		for position in self.filledPositions:
			if i == 1:
				positionString = "\'" + position + "\'"
			else:
				positionString = positionString + " AND Pos!=" + "\'" + position + "\'"
			i = i + 1
		return positionString

	def generateMaxedDraftString(self):
		positionString = ""
		i = 1
		for position in self.maxedPositions:
			if i == 1:
				positionString = "\'" + position + "\'"
			else:
				positionString = positionString + " AND Pos!=" + "\'" + position + "\'"
			i = i + 1
		return positionString

	def chooseNextPlayer(self):
		sqlHandler = SQL_HANDLER()
		if len(self.filledPositions) != 0 and len(self.filledPositions) < 6:
			excludedPositions = self.generateStarterDraftString()
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' AND Pos!=" + excludedPositions + " ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
		elif len(self.maxedPositions)==0:
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
			self.checkMaxedPositions()
		else:
			excludedPositions = self.generateMaxedDraftString()
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' AND Pos!=" + excludedPositions + " ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
			self.checkMaxedPositions()
		return data

	def addNextPlayer(self):	
		data = self.chooseNextPlayer(self.year)
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.team.addPlayer(newPlayer)
		self.updateList(self.year, newPlayer)