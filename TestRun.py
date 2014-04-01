from algorithmTester import *
from LocalSearchAlgorithm import *

algoTester = algorithmTester([localSearchAlgorithm(1), Algorithm(2), Algorithm(3), Algorithm(4), Algorithm(5), Algorithm(6), Algorithm(7), Algorithm(8), Algorithm(9), Algorithm(10)])
algoTester.runTest(2012)

x = 0
for a in algoTester.algorithms:
	x = x + 1
	# print a
	a.printTeam()