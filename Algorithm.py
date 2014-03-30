from MostFantasyPointsAlgorithm import *
from teamClass import *
import sqlite3 as lite

##########################################################################################
#
# CLASS: Algorithm
#
# Members: 		name of algorithm, team
#						
# Functions:	determineNextSelection - Decides which Player should be drafted next by this algorithm
#						args:		
#						returns:	Name of player
#
##########################################################################################

class Algorithm:
	def __init__(self):
		self.name = ""
		self.team = Team()
	def __init__(self, inputName):
		self.name = str(inputName)
		self.team = Team()
	def updateList(self, year, player):
		conn = lite.connect('ESPN.db')
		c = conn.cursor()
		command = "UPDATE DraftList_" + str(year) + " SET WasSelected=\'1\' WHERE Player=\'" + player.name + "\'"
		# print command
		c.execute(command)
		conn.commit()
		conn.close()
	def pickNextPlayer(self, year):
		sqlHandler = SQL_HANDLER()
		data = sqlHandler.CALL_SQL_SELECT("ESPN.db","Player, Pos, Points", "DraftList_"+str(year),"WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'")
		print data
		# command1 = "SELECT Player, Pos, Points FROM DraftList_"
		# command2 = " WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'"
		# conn = lite.connect('ESPN.db')
		# c = conn.cursor()
		# command = command1 + str(year) + command2 # Maybe pass this line into this version of the method (i.e. call super(pickNextPlayer(<THIS_STRING>)))
		# c.execute(command)
		# data = c.fetchall()
		# conn.close()
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		self.team.addPlayer(newPlayer)
		self.updateList(year, newPlayer)
	def printTeam(self):
		print "\n\n\nAlgorithm " + self.name
		self.team.printTeam()


