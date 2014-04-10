from algorithmTester import *
from LocalSearchAlgorithm import *
import time

startTime = time.time()
algoTester = algorithmTester([GreedyByPositionAlgorithm(1), GreedyByPositionAlgorithm(2), GreedyByPositionAlgorithm(3), GreedyByPositionAlgorithm(4), GreedyByPositionAlgorithm(5), GreedyByPositionAlgorithm(6), GreedyByPositionAlgorithm(7), GreedyByPositionAlgorithm(8), GreedyByPositionAlgorithm(9), GreedyByPositionAlgorithm(10)])
algoTester.runTest(2011)
endTime = time.time()

# x = 0
# for a in algoTester.algorithms:
# 	x = x + 1
# 	a.printTeam()

print "Member total points: " + str(algoTester.algorithms[0].team.getTotalPoints())
print "Member starter points: " + str(algoTester.algorithms[0].team.getStarterPoints())
print endTime - startTime, "seconds to simulate this draft"

print algoTester.algorithms[0].printTeam()