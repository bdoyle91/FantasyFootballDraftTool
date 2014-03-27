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
# Functions:	runTest - simulates a draft using this algorithmTester's list of algorithms
#						args:		year to be tested
#						returns:	
#
##########################################################################################
class algorithmTester:
	def __init__(self, algorithms):
		self.algorithms = algorithms
	def runTest(self, year):
		conn = lite.connect('ESPN.db')
		c = conn.cursor()
		command = "UPDATE DraftList_" + str(year) + " SET WasSelected = \'0\'"
		c.execute(command)
		conn.commit()
		conn.close()
		i = TEAM_SIZE
		while (i > 0):
			for eachAlgorithm in self.algorithms:
				eachAlgorithm.pickNextPlayer(year)
			i = i - 1
			if (i > 0):
				for algs in reversed(self.algorithms):
					algs.pickNextPlayer(year)
				i = i - 1