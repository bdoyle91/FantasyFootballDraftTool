from teamClass import *

#Team Instances
NUMBER_OF_TEAMS = 10

TEAM_LIST = []
for teamNum in range(NUMBER_OF_TEAMS):
	newTeam = Team()
	newTeam.setName(teamNum)
	TEAM_LIST.append(newTeam)