from algorithmTester import *
from LeagueTeams import *

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
		self.bestPoint = 0

	def __init__(self, inputName):
		self.name = ""
		self.team = Team()
		self.year = -1
		self.filledPositions = []
		self.maxedPositions = []
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []
		self.bestPoint = 0

	def __init__(self, inputName, inputNumOfTeams, inputStartingPosition):
		self.name = ""
		self.team = Team()
		self.year = -1
		self.filledPositions = []
		self.maxedPositions = []
		self.draftRound = 1
		self.draftSelectionsBeforeSearch = []
		self.bestPoint = 0
		self.numOfTeams = inputNumOfTeams
		self.startingposition = inputStartingPosition

	def saveDraftSelections(self):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, WasSelected", "DraftList_"+str(self.year))
		self.draftSelectionsBeforeSearch = data

	def returnDraftList(self):
		sqlHandler = SQL_HANDLER()
		for eachPlayer in self.draftSelectionsBeforeSearch:
			sqlHandler.CALL_SQL_UPDATE("ESPN.db","WasSelected",str(eachPlayer[1]),"DraftList_"+str(self.year), "Player", eachPlayer[0])

	def simulateRemainingDraft(self, newPlayer):
		searchAlgorithim = GreedyByPositionAlgorithm(1)
		searchAlgorithim.team.setYear(self.year)
		searchAlgorithim.setTeam(self.team)
		searchAlgorithim.team.addPlayer(newPlayer)
		#Save the current selections
		self.saveDraftSelections()

		#Create an algorithm instance 
		algoTester = algorithmTester()
		
		pos = 1
		#Check to see the round of the draft, if odd draft from your normal positions, otherwise invert
		if self.draftRound%2 == 1:
			while pos <= self.numOfTeams:
				#Check to see if it is this algorithm's draft slow (non-snaked)
				if pos == self.startingposition:
					algoTester.algorithms.append(searchAlgorithim)
				#otherwise insert a greedy algorithm
				else:
					newAlgo = GreedyByPositionAlgorithm(pos)
					newAlgo.team.setYear(self.year)
					newAlgo.setTeam(TEAM_LIST[pos-1])
					algoTester.algorithms.append(newAlgo)
				pos = pos + 1
		else:
			while pos <= self.numOfTeams:
				#Check to see if it is this algorithm's draft slow (snaked)
				if pos == (10-(self.startingposition-1)):
					algoTester.algorithms.append(searchAlgorithim)
				#otherwise insert a greedy algorithm
				else:					
					newAlgo = GreedyByPositionAlgorithm(10 - (pos-1))
					newAlgo.team.setYear(self.year)
					newAlgo.setTeam(TEAM_LIST[pos-1])
					algoTester.algorithms.append(newAlgo)
				pos = pos + 1
		#Simulate the rest of the draft
		algoTester.runTest(self.year, False, self.draftRound)

		#Check starter points
		points = searchAlgorithim.team.getStarterPoints()

		#Set the draft back to how it was before we simulated
		self.returnDraftList()
		return points

	def chooseNextPlayer(self):
		sqlHandler = SQL_HANDLER()
		print "------------------- Pick Number " + str(self.draftRound) + "----------------------"
		#Check Each Position and simulate rest of draft, draft position that yields highest result
		for eachPosition in POSITIONLIST:
			data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(self.year),"WHERE WasSelected=\'0\' AND Pos == \'" + eachPosition + "\' ORDER BY Points DESC LIMIT \'1\'")
			newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
			newPoint = self.simulateRemainingDraft(newPlayer)
			if newPoint > self.bestPoint:
				self.bestPoint = newPoint
				playerToAdd = data
			self.checkFilledPositions()
		data = playerToAdd
		self.bestPoint = 0
		self.draftRound = self.draftRound + 1
		return data