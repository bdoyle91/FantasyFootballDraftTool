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
#
#
##########################################################################################
class algorithmTester:
	def __init__(self, algorithms):
		self.algorithms = algorithms
	def clearDraftList(self,year):
		conn = lite.connect('ESPN.db')
		c = conn.cursor()
		command = "UPDATE DraftList_" + str(year) + " SET WasSelected = \'0\'"
		c.execute(command)
		conn.commit()
		conn.close()
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