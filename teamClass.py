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

class Player:
	def __init__(self, fullName, position, points):
		self.name = fullName
		self.pos = position
		self.fantasyPoints = points