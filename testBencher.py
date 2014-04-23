import teamClass
import sqlite3 as lite

#	This script is used to create benchmarks for the drafts of top
#	

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

def benchMark(players, year="2013"):
	conn = lite.connect('ESPN.db')
	benchTeam = teamClass.Team()
	for player in players:
		c = conn.cursor()
		command = "SELECT Player,Pos,Points FROM FantasyPoints_" + str(year) + " WHERE Player='" + str(player) + "'"
		c.execute(command)
		data = c.fetchall()
		print data
		newPlayer = teamClass.Player(data[0][0], int(data[0][2]), data[0][1])
		print "newPlayer " + str(newPlayer)
		benchTeam.addPlayer(newPlayer)
	conn.close()
	points = benchTeam.starterPoints
	print benchTeam.printTeam()
	return points


#########################################################################################
#	Testing Teams Consisting of Following:
#	1 QB
#	2 RB
#	2 WR
#	1 TE
#	1 FLEX
#	1 DEF
#	1 K
######### UNIT TEST MAIN ################################################################

CHITRADER2 = ["Jamaal Charles","Matt Forte","Demaryius Thomas","Jimmy Graham","Montee Ball","Russell Wilson","Antonio Brown","T.Y. Hilton","Cecil Shorts", "Andre Brown","Chicago","Jonathan Dwyer","Michael Vick","Bryce Brown","Matt Prater","Johnathan Franklin"]
CHITRADER2pick = 6
benchMark(CHITRADER2)
TEAMJENKINS = ["Calvin Johnson","Dez Bryant","Jimmy Graham","Peyton Manning","Isaac Redman","Wes Welker","Houston","Ahmad Bradshaw","Shane Vereen","Knowshon Moreno","Stephen Gostkowski","Lance Moore","Kenny Britt","Denarius Moore","Fred Jackson","Sam Bradford"]
TEAMJENKINSpick = 10
benchMark(TEAMJENKINS)
#print benchPoints

