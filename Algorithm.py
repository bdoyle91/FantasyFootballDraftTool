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
	def updateList(self, year, player):
		conn = lite.connect('ESPN.db')
		c = conn.cursor()
		command = "UPDATE DraftList_" + str(year) + " SET WasSelected=\'1\' WHERE Player=\'" + player.name + "\'"
		# print command
		c.execute(command)
		conn.commit()
		conn.close()
	def pickNextPlayer(self, year, command1 = "SELECT Player, Pos, Points FROM DraftList_", command2 = " WHERE WasSelected=\'0\' ORDER BY Points DESC LIMIT \'1\'"):
		conn = lite.connect('ESPN.db')
		c = conn.cursor()
		command = command1 + str(year) + command2 # Maybe pass this line into this version of the method (i.e. call super(pickNextPlayer(<THIS_STRING>)))
		# print command
		c.execute(command)
		print command
		data = c.fetchall()
		conn.close()
		print "data00 " + str(data[0][0]) 
		print " data01 " + str(data[0][1]) 
		print "data02" + str(data[0][2])
		newPlayer = Player(data[0][0], int(data[0][2]), data[0][1])
		print "data: " + str(data)
		# print "newPlayer: " + str(newPlayer.name)
		self.team.addPlayer(newPlayer)
		self.updateList(year, newPlayer)

	def printTeam(self, algorithmNumber):
		print "\n\n\nAlgorithm " + str(algorithmNumber)
		self.team.printTeam()

##########################################################################################
#
# CLASS: PARAlgorithm (Points Above Replacement) extends Algorithm
#
# Members: 		name of algorithm, team
#						
# Functions:	determineNextSelection - Decides which Player should be drafted next by this algorithm, 
#										 based on the remaining players' PAR compared to other players at their position.
#						args:		year
#						returns:	Name of player
#
##########################################################################################

# class PARAlgorithm(Algorithm):
#     def __init__(self):
#         super(PARAlgorithm, self).__init__()
# 	def pickNextPlayer(self, year):
# 		command = "SELECT Player, Pos, MAX(Points) FROM DraftList_" + str(year) + " WHERE WasSelected=\'0\'" # Maybe pass this line into this version of the method (i.e. call super(pickNextPlayer(<THIS_STRING>)))
# 		super(PARAlgorithm, self).pickNextPlayer()



