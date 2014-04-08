from LeagueSettings import *

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
		self.DEFs = []
		self.year = -1
		self.starterPoints = 0
		self.totalPoints = 0

	def setYear(self, inputYear):
		self.year = inputYear

	def addPlayer(self, x):
		if x.pos.strip() == "QB":
			self.QBs.append(x)
		elif (x.pos.strip() == "RB") or (x.pos.strip() == "FB"):
			self.RBs.append(x)
		elif x.pos.strip() == "WR":
			self.WRs.append(x)
		elif x.pos.strip() == "TE":
			self.TEs.append(x)
		elif x.pos.strip() == "PK":
			self.PKs.append(x)
		else:
			self.DEFs.append(x)
		self.totalPoints = self.totalPoints + x.fantasyPoints
		
	def getTotalPoints(self):
		return self.totalPoints

	def getStarterPoints(self):
		points = 0
		i = 1
		for player in self.QBs:
			if i > STARTING_QBS:
				break
			points = points + player.fantasyPoints
			i = i + 1
		i = 1
		for player in self.RBs:
			if i > STARTING_RBS:
				break
			points = points + player.fantasyPoints
			i = i + 1
		i = 1
		for player in self.WRs:
			if i > STARTING_WRS:
				break
			points = points + player.fantasyPoints
			i = i + 1
		i = 1
		for player in self.TEs:
			if i > STARTING_TES:
				break
			points = points + player.fantasyPoints
			i = i + 1
		i = 1
		for player in self.PKs:
			if i > STARTING_KS:
				break
			points = points + player.fantasyPoints
			i = i + 1
		i = 1
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
		print "\n\nDefenses\n"
		for player in self.DEFs:
			print player.name + ", " + player.pos + ", " + str(player.fantasyPoints)
		print "\nTotal Points: " + str(self.getTotalPoints())
		print "Total Starter Points: " + str(self.getStarterPoints()) + "\n"

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