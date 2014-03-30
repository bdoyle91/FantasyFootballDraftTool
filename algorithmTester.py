from teamClass import *
from Algorithm import *
import sqlite3 as lite
from MostFantasyPointsAlgorithm import *

##########################################################################################
#
# CLASS: algorithmTester
#
# Members: 		algorithms
#						
#
#
##########################################################################################
class algorithmTester:
	def __init__(self, algorithms):
		self.algorithms = algorithms
	def clearDraftList(self,year):
		sqlHandler = SQL_HANDLER()
		sqlHandler.CALL_SQL_UPDATE("ESPN.db","WasSelected","0","DraftList_2012")
	def runTest(self, year, clear=True, currentDraftPick=1):
		if clear==True:
			self.clearDraftList(year)
		i = TEAM_SIZE - (currentDraftPick-1)
		while (i > 0):
			for eachAlgorithm in self.algorithms:
				eachAlgorithm.pickNextPlayer(year)
			i = i - 1
			if (i > 0):
				for algs in reversed(self.algorithms):
					algs.pickNextPlayer(year)
				i = i - 1