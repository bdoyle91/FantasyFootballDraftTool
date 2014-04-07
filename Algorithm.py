from SQLHandler import *
from teamClass import *

##########################################################################################
#
# CLASS: Algorithm
#
# Members: 		name of algorithm, team
#						
# Functions:	addNextPlayer - Decides which Player should be drafted next by this algorithm
#						args:		
#						returns:	Name of player
#
##########################################################################################

class Algorithm:
	def __init__(self):
		self.name = ""
		self.team = Team()
		self.year = -1

	def __init__(self, inputName):
		self.name = str(inputName)
		self.team = Team()
		self.year = -1

	def setYear(self, inputYear):
		self.year = inputYear

	def updateList(self, player):
		sqlHandler = SQL_HANDLER()
		sqlHandler.CALL_SQL_UPDATE("ESPN.db","WasSelected","1","DraftList_"+str(self.year),"Player",player.name)

	def chooseNextPlayer(self):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
		return data

	def addNextPlayer(self):	
		data = self.chooseNextPlayer(self.year)
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.team.addPlayer(newPlayer)
		self.updateList(self.year, newPlayer)

	def printTeam(self):
		print "\n\n\nAlgorithm " + self.name
		self.team.printTeam()


