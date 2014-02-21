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

		

algoTester = algorithmTester([Algorithm(), Algorithm(), Algorithm(), Algorithm(), Algorithm(), Algorithm(), Algorithm(), Algorithm(), Algorithm(), Algorithm()])
algoTester.runTest(2012)

x = 0
for a in algoTester.algorithms:
	x = x + 1
	# print a
	print "Algorithm " + str(x)
	for player in a.team.Players:
	 	print player.name
