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
	playerlist = []
	for player in players:
		c = conn.cursor()
		print player
		command = "SELECT Player,Pos,Points FROM FantasyPoints_" + str(year) + " WHERE Player='" + str(player) + "'"
		c.execute(command)
		data = c.fetchall()
		if data == []:
			newData = [player, 0, "QB"]
		else:
			newData = [data[0][0], int(data[0][2]), data[0][1]]
		playerlist.append(newData)
	print playerlist
	playerlist.sort(key = lambda row: row[1])
	print playerlist
	print "-----------"
	playerlist.reverse()
	print playerlist
	for data in playerlist:
		print data
		newPlayer = teamClass.Player(data[0], int(data[1]), data[2])
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

BEST1ST = ["Adrian Peterson","Peyton Manning", "Brandon Marshall", "Vernon Davis", "David Wilson", "Jordy Nelson", "Seattle", "Golden Tate", "Stephen Gostkowski", "Tony Romo", "Mark Ingram", "Martellus Bennett", "Andre Brown", "Rueben Randle","Brandon Lloyd","Dwayne Allen"]
BEST2ND = ["Peyton Manning","Jamaal Charles", "DeMarco Murray", "Chris Johnson", "Blair Walsh", "Vincent Jackson", "Pierre Garcon", "Lamar Miller", "Alshon Jeffery", "Steve Johnson", "Cincinnati", "Michael Vick", "Jordan Cameron", "Knowshon Moreno", "Rueben Randle", "Brandon Myers"]
BEST3RD = ["Doug Martin", "Julio Jones", "Jimmy Graham", "Reggie Bush", "Antonio Brown", "Giovani Bernard", "Andrew Luck", "San Francisco", "Anquan Boldin", "Stephen Gostkowski", "Golden Tate", "Josh Gordon", "DeAndre Hopkins", "Denver", "Phil Dawson", "Greg Little"]
BEST4TH = ["Marshawn Lynch","Peyton Manning","Matt Forte","Larry Fitzgerald","Marques Colston", "Dennis Pitta", "Danny Amendola", "Chicago", "Stephen Gostkowski", "Vick Ballard", "Miles Austin", "Michael Vick","Martellus Bennett", "Cincinnati","Greg Zuerlein","Jacquizz Rodgers"]
BEST5TH = ["Peyton Manning","A.J. Green","Matt Forte","Jimmy Graham","Darren McFadden","Ahmad Bradshaw", "Chicago","Anquan Boldin","Lamar Miller","Phil Dawson","Mike Williams","Fred Jackson","Lance Moore","Josh Freeman","Brandon Myers","Kenbrell Thompkins"]
BEST6TH = ["Jamaal Charles", "Peyton Manning", "Dez Bryant", "Frank Gore","Marques Colston","Jason Witten","Ahmad Bradshaw", "Jordy Nelson", "New England", "Stephen Gostkowski","Mike Williams","Knowshon Moreno","Denarius Moore","Bernard Pierce","Jacquizz Rodgers","Andy Dalton"]
BEST7TH = ["Calvin Johnson","Peyton Manning","Jimmy Graham","Vincent Jackson","DeMarco Murray","Seattle","Ryan Mathews","Miles Austin","Brandon Myers","Michael Vick","Matt Prater","Kenny Britt","Isaac Redman", "St. Louis", "Sebastian Janikowski","Knowshon Moreno"]
BEST8TH = ["Jamaal Charles","LeSean McCoy","Jimmy Graham","Randall Cobb","Danny Amendola","Eddie Lacy","DeSean Jackson","Andrew Luck","Miles Austin","Josh Gordon","San Francisco","Johnathan Franklin","Michael Vick","Coby Fleener","Ronnie Hillman","Sebastian Janikowski"]
BEST9TH = ["Jamaal Charles", "LeSean McCoy", "Jimmy Graham", "Demaryius Thomas", "Reggie Wayne", "Matthew Stafford", "Giovani Bernard", "DeSean Jackson", "Shane Vereen", "San Francisco", "Josh Gordon", "Golden Tate", "Jared Cook", "Shonn Greene", "Malcom Floyd","Phil Dawson"]
BEST10TH = ["Jamaal Charles","LeSean McCoy", "Brandon Marshall", "Jimmy Graham", "Robert Griffin III", "Matthew Stafford", "Jordy Nelson","Montee Ball","Russell Wilson", "Mike Williams", "Chicago", "Bryce Brown", "New England", "Brandon Pettigrew", "Felix Jones", "Matt Prater"]
BESTPOSSIBLE = ["Peyton Manning", "Drew Brees", "Jamaal Charles", "LeSean McCoy", "Matt Forte", "Knowshon Moreno","Josh Gordon","Demaryius Thomas","Calvin Johnson","A.J. Green","Alex Smith", "Jimmy Graham","Carolina", "Seattle","Stephen Gostkowski","Matt Prater"]
# benchMark(BEST1ST)
# benchMark(BEST2ND)
# benchMark(BEST3RD)
# benchMark(BEST4TH)
# benchMark(BEST5TH)
# benchMark(BEST6TH)
# benchMark(BEST7TH)
# benchMark(BEST8TH)
# benchMark(BEST9TH)
# benchMark(BEST10TH)
benchMark(BESTPOSSIBLE)