from LeagueSettings import *
from SQLHandler import *
import traceback

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
		self.starterProjectedPoints = 0
		self.starterPointsNextYear = 0
		self.name = ""

	def resetTeam(self):
		self.QBs = []
		self.RBs = []
		self.WRs = []
		self.TEs = []
		self.PKs = []
		self.DEFs = []
		self.starterPoints = 0
		self.totalPoints = 0
		self.starterProjectedPoints = 0
		self.starterPointsNextYear = 0

	def setYear(self, inputYear):
		self.year = inputYear

	def setName(self, inputName):
		self.name = inputName
		
	def addPlayer(self, x):
		startingValue = 0
		projectedStarterValue = 0
		actualStarterValue = 0
		#It isn't necessary to to set the year for most functionality to work, added a
		#warning if this has been neglated including exact callstack
		if self.year == -1:
			print "WARNING IN addPlayer in Team Instance " + str(self) + ", year not set"
			traceback.print_stack()
		else:
			x.setYear(self.year)
			x.lookupProjectedPointsPerfect()
			x.lookupNextYearPoints()
		if x.pos.strip() == "QB":
			if len(self.QBs) < len(GP_QBS):
				startingValue = (x.fantasyPoints/16)*GP_QBS[len(self.QBs)]
				projectedStarterValue = (x.projectedPoints/16)*GP_QBS[len(self.QBs)]
				actualStarterValue = (x.actualPoints/16)*GP_QBS[len(self.QBs)]
			self.QBs.append(x)
		elif (x.pos.strip() == "RB") or (x.pos.strip() == "FB"):
			if len(self.RBs) < len(GP_RBS):
				startingValue = (x.fantasyPoints/16)*GP_RBS[len(self.RBs)]
				projectedStarterValue = (x.projectedPoints/16)*GP_RBS[len(self.RBs)]
				actualStarterValue = (x.actualPoints/16)*GP_RBS[len(self.RBs)]
			self.RBs.append(x)
		elif x.pos.strip() == "WR":
			if len(self.WRs) < len(GP_WRS):
				startingValue = (x.fantasyPoints/16)*GP_WRS[len(self.WRs)]
				projectedStarterValue = (x.projectedPoints/16)*GP_WRS[len(self.WRs)]
				actualStarterValue = (x.actualPoints/16)*GP_WRS[len(self.WRs)]
			self.WRs.append(x)
		elif x.pos.strip() == "TE":
			if len(self.TEs) < len(GP_TES):
				startingValue = (x.fantasyPoints/16)*GP_TES[len(self.TEs)]
				projectedStarterValue = (x.projectedPoints/16)*GP_TES[len(self.TEs)]
				actualStarterValue = (x.actualPoints/16)*GP_WRS[len(self.WRs)]
			self.TEs.append(x)
		elif x.pos.strip() == "PK":
			if len(self.PKs) < len(GP_KS):
				startingValue = (x.fantasyPoints/16)*GP_KS[len(self.PKs)]
				projectedStarterValue = (x.projectedPoints/16)*GP_KS[len(self.PKs)]
				actualStarterValue = (x.actualPoints/16)*GP_KS[len(self.PKs)]
			self.PKs.append(x)
		else:
			if len(self.DEFs) < len(GP_DSTS):
				startingValue = (x.fantasyPoints/16)*GP_DSTS[len(self.DEFs)]
				projectedStarterValue = (x.projectedPoints/16)*GP_DSTS[len(self.DEFs)]
				actualStarterValue = (x.actualPoints/16)*GP_DSTS[len(self.DEFs)]
			self.DEFs.append(x)
		self.totalPoints = self.totalPoints + x.fantasyPoints
		self.starterPoints = self.starterPoints + startingValue
		self.starterProjectedPoints = self.starterProjectedPoints + projectedStarterValue
		self.starterPointsNextYear = self.starterPointsNextYear + actualStarterValue
	def getTotalPoints(self):
		return self.totalPoints

	def getStarterPoints(self):
		return self.starterPoints

	def getStarterPointsNextYear(self):
		return self.starterPointsNextYear 

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
		self.year = -1
		self.projectedPoints = -1
		self.actualPoints = -1

	def setYear(self, inputYear):
		self.year = inputYear

	def lookupProjectedPointsPerfect(self):
		if self.year == -1:
			return -1
		handler = SQL_HANDLER()
		projection = handler.CALL_SQL_SELECT("ESPN.db","Points","FantasyPoints_"+str(self.year+1),"WHERE Player = \'" + self.name + "\'")
		if projection == []:
			self.projectedPoints = 0
		else:
			self.projectedPoints = projection[0][0]

	def lookupNextYearPoints(self):
		if self.year == -1:
			return -1
		handler = SQL_HANDLER()
		projection = handler.CALL_SQL_SELECT("ESPN.db","Points","FantasyPoints_"+str(self.year+1),"WHERE Player = \'" + self.name + "\'")
		if projection == []:
			self.actualPoints = 0
		else:
			self.actualPoints = projection[0][0]