from algorithmTester import *
from LocalSearchAlgorithm import *
from LeagueTeams import *
import time

print TEAM_LIST

searchAlgoPosition = 1

# for number in range(0,10):
# 	algoTester = algorithmTester()
# 	for number2 in range(0,10):
# 		if number == number2:
# 			algoTester.algorithms.append(LocalSearchAlgorithm("LOCALSEARCH", 10, number))
# 		else:
# 			algoTester.algorithms.append(GreedyByPositionAlgorithm("Greedy " + str(number2)))
# 	print algoTester.algorithms
# 	algoTester.runTest(2011)
# 	x=0
# 	for a in algoTester.algorithms:
# 	 	x = x + 1
#  		print "Algorithm Name: " + str(a.name)
#  		print "Member total points: " + str(a.team.getTotalPoints())
#  		print "Member starter points: " + str(a.team.getStarterPoints())

algoTester = algorithmTester()
for teamNum in range(0, NUMBER_OF_TEAMS)
	if teamNum == (searchAlgoPosition - 1)
		algoTester.algorithms.append(LocalSearchAlgorithm("LOCALSEARCH", NUMBER_OF_TEAMS, number))
	else:
		algoTester.algorithms.append(GreedyByPositionAlgorithm())

algoTester = algorithmTester([LocalSearchAlgorithm("LOCALSEARCH", 10, searchPosition), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm(), GreedyByPositionAlgorithm()])
teamCounter = 0
for eachAlgorithm in algoTester.algorithms:
	eachAlgorithm.team = TEAM_LIST[teamCounter]
	if teamCounter == (searchAlgoPosition - 1):
		eachAlgorithm.team.setName("LocalSearch Team Draft Position " + str(teamCounter+1))
	else:
		eachAlgorithm.team.setName("Greedy Team Draft Position " + str(teamCounter+1))
	teamCounter = teamCounter + 1

for eachAlgorithm in algoTester.algorithms:
	print eachAlgorithm.team 

algoTester.runTest(2011)

x = 0
for a in algoTester.algorithms:
	x = x + 1
	print "Algorithm Name: " + str(a.team.name)
	print "Member total points: " + str(a.team.getTotalPoints())
	print "Member starter points: " + str(a.team.getStarterPoints())


# print "Member total points: " + str(algoTester.algorithms[0].team.getTotalPoints())
# print "Member starter points: " + str(algoTester.algorithms[0].team.getStarterPoints())
# print endTime - startTime, "seconds to simulate this draft"
# print algoTester.algorithms[0].printTeam()