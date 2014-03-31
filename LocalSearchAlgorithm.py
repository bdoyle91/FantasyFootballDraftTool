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

	def pickNextPlayer(self, year):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.team.addPlayer(newPlayer)
		self.updateList(year, newPlayer)
		self.draftRound = self.draftRound + 1
		self.saveDraftSelections(year)

	def saveDraftSelections(self, year):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, WasSelected", "DraftList_"+str(year))
		self.draftSelectionsBeforeSearch = data

algoTester = algorithmTester([localSearchAlgorithm(1), Algorithm(2), Algorithm(3), Algorithm(4), Algorithm(5), Algorithm(6), Algorithm(7), Algorithm(8), Algorithm(9), Algorithm(10)])
algoTester.runTest(2012)

x = 0
for a in algoTester.algorithms:
	x = x + 1
	# print a
	a.printTeam()