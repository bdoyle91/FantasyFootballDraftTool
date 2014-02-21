import teamClass
import sqlite3 as lite

##########################################################################################
#
# ** benchMark **
#
# Arguments: 	List of player names and year to be evaluated
# Function: 	Stores all the players in a Team class and then evalutes
#				using built in function
# Returns: 		Tean Fantasy Points
#
#
##########################################################################################

def benchMark(players, year="2012"):
	conn = lite.connect('ESPN.db')
	benchTeam = teamClass.Team()
	for player in players:
		c = conn.cursor()
		command = "SELECT Player,Points FROM FantasyPoints_" + str(year) + " WHERE Player='" + str(player) + "'"
		c.execute(command)
		data = c.fetchall()
		newPlayer = teamClass.Player(data[0][0],int(data[0][1]))
		benchTeam.addPlayer(newPlayer)
	conn.close()
	points = benchTeam.getTotalPoints()
	return points


#########################################################################################
#	Testing Teams Consisting of Following:
#	1 QB
#	2 RB
#	2 WR
#	1 TE
#	1 FLEX
#	1 DEF 	< - We don't have stats yet cannot implement
#	1 K		< - We don't have stats yet cannot implement
######### UNIT TEST MAIN ################################################################

Players = ["Peyton Manning","Ray Rice","Reggie Bush","Dez Bryant","Greg Jennings","Jason Witten","Rashard Mendenhall"]
benchPoints = benchMark(Players)
print benchPoints

