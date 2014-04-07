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

class LocalSearchAlgorithm(GreedyByPositionAlgorithm):
	def __init__(self):
		self.name = ""
		self.team = Team()
		self.year = -1
		self.filledPositions = []
		self.maxedPositions = []
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []

	def __init__(self, inputName):
		self.name = ""
		self.team = Team()
		self.year = -1
		self.filledPositions = []
		self.maxedPositions = []
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []

	def saveDraftSelections(self):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, WasSelected", "DraftList_"+str(self.year))
		self.draftSelectionsBeforeSearch = data

	def simulateRemainingDraft(self, newPlayer):
		searchAlgorithim = GreedyByPositionAlgorithm(1)
		searchAlgorithim.setTeam(self.team)
		searchAlgorithim.team.addPlayer(newPlayer)
		searchAlgorithim.printTeam()

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
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.simulateRemainingDraft(newPlayer)
		return data