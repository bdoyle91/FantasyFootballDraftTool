from algorithmTester import *

##########################################################################################
#
# CLASS: localSearchAlgorithm
#
# Members: 		name of algorithm, team
#						
# Functions:	determineNextSelection - Decides which Player should be drafted next by this algorithm
#						args:		
#						returns:	Name of player
#
##########################################################################################

class localSearchAlgorithm(Algorithm):
	def __init__(self):
		self.name = ""
		self.team = Team()
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []

	def __init__(self, inputName):
		self.name = str(inputName)
		self.team = Team()		
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []

	def addNextPlayer(self, year):
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.team.addPlayer(newPlayer)
		self.updateList(year, newPlayer)
		self.draftRound = self.draftRound + 1
		self.saveDraftSelections(year)

	def saveDraftSelections(self, year):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, WasSelected", "DraftList_"+str(year))
		self.draftSelectionsBeforeSearch = data



