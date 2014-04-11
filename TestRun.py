from algorithmTester import *
from LocalSearchAlgorithm import *
import time

#for number in range(0,10)
algoTester = algorithmTester([LocalSearchAlgorithm("LOCALSEARCH", 10, 10), GreedyByPositionAlgorithm("Greedy 1"), GreedyByPositionAlgorithm("Greedy 2"), GreedyByPositionAlgorithm("Greedy 3"), GreedyByPositionAlgorithm("Greedy 4"), GreedyByPositionAlgorithm("Greedy 5"), GreedyByPositionAlgorithm("Greedy 6"), GreedyByPositionAlgorithm("Greedy 7"), GreedyByPositionAlgorithm("Greedy 8"), GreedyByPositionAlgorithm("Greedy 9")])
algoTester.runTest(2011)

x = 0
for a in algoTester.algorithms:
	x = x + 1
	print "Algorithm Name: " + str(a.name)
	print "Member total points: " + str(a.team.getTotalPoints())
	print "Member starter points: " + str(a.team.getStarterPoints())


# print "Member total points: " + str(algoTester.algorithms[0].team.getTotalPoints())
# print "Member starter points: " + str(algoTester.algorithms[0].team.getStarterPoints()))
# print endTime - startTime, "seconds to simulate this draft"
# print algoTester.algorithms[0].printTeam()