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
		self.filledPositions = []
		self.maxedPositions = []
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []

	def __init__(self, inputName):
		self.name = ""
		self.team = Team()
		self.filledPositions = []
		self.maxedPositions = []
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []

	def saveDraftSelections(self, year):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, WasSelected", "DraftList_"+str(year))
		self.draftSelectionsBeforeSearch = dat

	def chooseNextPlayer(self, year):
		sqlHandler = SQL_HANDLER()
		if len(self.filledPositions) != 0 and len(self.filledPositions) < 6:
			excludedPositions = self.generateStarterDraftString()
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' AND Pos!=" + excludedPositions + " ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
		elif len(self.maxedPositions)==0:
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
			self.checkMaxedPositions()
		else:
			excludedPositions = self.generateMaxedDraftString()
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' AND Pos!=" + excludedPositions + " ORDER BY Points DESC LIMIT \'1\'")
			self.checkFilledPositions()
			self.checkMaxedPositions()
		return data



