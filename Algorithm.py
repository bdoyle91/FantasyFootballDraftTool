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
		print command
		c.execute(command)
		conn.commit()
		conn.close()
	def pickNextPlayer(self, year):
		conn = lite.connect('ESPN.db')
		c = conn.cursor()
		command = "SELECT Player, MAX(Points) FROM DraftList_" + str(year) + " WHERE WasSelected=\'0\'"
		print command
		c.execute(command)
		data = c.fetchall()
		conn.close()
		newPlayer = Player(data[0][0], int(data[0][1]))
		print "data: " + str(data)
		print "newPlayer: " + str(newPlayer.name)
		self.team.addPlayer(newPlayer)
		self.updateList(year, newPlayer)