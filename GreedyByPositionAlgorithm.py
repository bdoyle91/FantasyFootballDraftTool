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
		self.projectionUse = False

	def __init__(self, inputName, inputProjectionUse=False):
		self.name = str(inputName)
		self.team = Team()
		self.year = -1
		self.filledPositions = []
		self.maxedPositions = []
		self.projectionUse = inputProjectionUse

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
				if self.projectionUse == False:
					positionString = positionString + " AND Pos!=" + "\'" + position + "\'"
				else:
					positionString = positionString + " AND DraftList_" + str(self.year+1) + ".Pos!=" + "\'" + position + "\'"
			i = i + 1
		return positionString

	def generateMaxedDraftString(self):
		positionString = ""
		i = 1
		for position in self.maxedPositions:
			if i == 1:
				positionString = "\'" + position + "\'"
			else:
				if self.projectionUse == False:
					positionString = positionString + " AND Pos!=" + "\'" + position + "\'"
				else:
					positionString = positionString + " AND DraftList_" + str(self.year+1) + ".Pos!=" + "\'" + position + "\'"
			i = i + 1
		return positionString

	def chooseNextPlayer(self):
		sqlHandler = SQL_HANDLER()
		#The case that handles if at least 1 starting position has been filled
		#but not all starting positions have been filled
		if len(self.filledPositions) != 0 and len(self.filledPositions) < 6:
			#Generate string based on filled starters
			excludedPositions = self.generateStarterDraftString()
			if self.projectionUse == False:
				data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' AND Pos!=" + excludedPositions + " ORDER BY Points DESC LIMIT \'1\'")
			else:
				data = sqlHandler.CALL_SQL_SELECT("ESPN.db","DraftList_" + str(self.year) + ".Player, DraftList_" + str(self.year) + ".Pos, DraftList_" + str(self.year) + ".Points", "DraftList_"+str(self.year),"INNER JOIN DraftList_" + str(self.year+1) + " ON  DraftList_"+str(self.year)+".Player== DraftList_"+str(self.year+1)+".Player WHERE DraftList_" + str(self.year+1) + ".Pos != " + excludedPositions + " AND DraftList_" + str(self.year)+ ".WasSelected=\'0\' ORDER BY DraftList_"+str(self.year+1)+ ".Points DESC LIMIT \'1\' ")
		
			#Check if all starting positions are filled
			self.checkFilledPositions()
		#Otherwise if no positons are maxed request any position
		elif len(self.maxedPositions)==0:
			if self.projectionUse == False:
				data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
			else:
				data = sqlHandler.CALL_SQL_SELECT("ESPN.db","DraftList_" + str(self.year) + ".Player, DraftList_" + str(self.year) + ".Pos, DraftList_" + str(self.year) + ".Points", "DraftList_"+str(self.year),"INNER JOIN DraftList_" + str(self.year+1) + " ON  DraftList_"+str(self.year)+".Player== DraftList_"+str(self.year+1)+".Player WHERE DraftList_" + str(self.year)+ ".WasSelected=\'0\' ORDER BY DraftList_"+str(self.year+1)+ ".Points DESC LIMIT \'1\' ")
			#Check if all starting positions are filled or if any positions are maxed
			self.checkFilledPositions()
			self.checkMaxedPositions()
		#If positions are maxed exclude maxed positions
		else:
			#Generate string based on maxed positions
			excludedPositions = self.generateMaxedDraftString()
			if self.projectionUse == False:
				data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' AND Pos!=" + excludedPositions + " ORDER BY Points DESC LIMIT \'1\'")
			else:
				data = sqlHandler.CALL_SQL_SELECT("ESPN.db","DraftList_" + str(self.year) + ".Player, DraftList_" + str(self.year) + ".Pos, DraftList_" + str(self.year) + ".Points", "DraftList_"+str(self.year),"INNER JOIN DraftList_" + str(self.year+1) + " ON  DraftList_"+str(self.year)+".Player== DraftList_"+str(self.year+1)+".Player WHERE DraftList_" + str(self.year+1) + ".Pos != " + excludedPositions + " AND DraftList_" + str(self.year)+ ".WasSelected=\'0\' ORDER BY DraftList_"+str(self.year+1)+ ".Points DESC LIMIT \'1\' ")
		
			#Check if all starting positions are filled or if any positions are maxed
			self.checkFilledPositions()
			self.checkMaxedPositions()
		return data