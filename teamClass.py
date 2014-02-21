##########################################################################################
#
# CLASS: Team
#
# Members: 		List of class "Player"
#						
# Functions:	addPlayer - 		Adds a Player to the team,
#						args:		Player x
#						returns:	None
#				getTotalPoints - 	Returns total number of points earned by
#									players, does not yet account for weekly collisions
#									or position collisions
#						args:		None
#						returns:	Points (integer)
#
##########################################################################################

class Team:
	def __init__(self):
		self.Players = []
	def addPlayer(self, x):
		self.Players.append(x)
	def getTotalPoints(self):
		points = 0
		for player in self.Players:
			points = points + player.fantasyPoints
		return points

##########################################################################################
#
# CLASS: Player
#
# Members: 		name 	- First and Last Name of People
#				pos 	- Position of Player
#				points 	- total number of fantasy points earned by the player
#
#
##########################################################################################

class Player:
	def __init__(self, fullName, points, position=""):
		self.name = fullName
		self.pos = position
		self.fantasyPoints = points