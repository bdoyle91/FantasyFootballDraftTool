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
		self.QBs = []
		self.RBs = []
		self.WRs = []
		self.TEs = []
		self.PKs = []

	def addPlayer(self, x):
		if x.pos.strip() == "QB":
			self.QBs.append(x)
		elif (x.pos.strip() == "RB") or (x.pos.strip() == "FB"):
			self.RBs.append(x)
		elif x.pos.strip() == "WR":
			self.WRs.append(x)
		elif x.pos.strip() == "TE":
			self.TEs.append(x)
		else:
			self.PKs.append(x)
		
	def getTotalPoints(self):
		points = 0
		for player in self.QBs:
			points = points + player.fantasyPoints
		for player in self.RBs:
			points = points + player.fantasyPoints
		for player in self.WRs:
			points = points + player.fantasyPoints
		for player in self.TEs:
			points = points + player.fantasyPoints
		for player in self.PKs:
			points = points + player.fantasyPoints
		return points

	def printTeam(self):
		print "\n\nQuarterbacks\n"
		for player in self.QBs:
			print player.name + ", " + player.pos + ", " + str(player.fantasyPoints)
		print "\n\nRunning Backs\n"
		for player in self.RBs:
			print player.name + ", " + player.pos + ", " + str(player.fantasyPoints)
		print "\n\nWide Receivers\n"
		for player in self.WRs:
			print player.name + ", " + player.pos + ", " + str(player.fantasyPoints)
		print "\n\nTight Ends\n"
		for player in self.TEs:
			print player.name + ", " + player.pos + ", " + str(player.fantasyPoints)
		print "\n\nKickers\n"
		for player in self.PKs:
			print player.name + ", " + player.pos + ", " + str(player.fantasyPoints)
		print "Total Points: " + str(self.getTotalPoints()) + "\n"

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