from algorithmTester import *
from LocalSearchAlgorithm import *
from LeagueTeams import *
import time
import os



def runSimulation(searchAlgoPosition, testYear):
	#Construct Results file
	fileTimeStamp = time.time()
	
	#Construct algorithm list
	algoTester = algorithmTester()
	for teamNum in range(0, NUMBER_OF_TEAMS):
		if teamNum == (searchAlgoPosition - 1):
			# algoTester.algorithms.append(LocalSearchAlgorithm("LOCALSEARCH", NUMBER_OF_TEAMS, teamNum, True))
			algoTester.algorithms.append(GreedyByPositionAlgorithm("Greedy",True))
		else:
			algoTester.algorithms.append(GreedyByPositionAlgorithm("Greedy",True))

	#Organize team instances
	teamCounter = 0
	for eachAlgorithm in algoTester.algorithms:
		eachAlgorithm.team = TEAM_LIST[teamCounter]
		if teamCounter == (searchAlgoPosition - 1):
			# eachAlgorithm.team.setName("LocalSearch Team Draft Position " + str(teamCounter+1))
			eachAlgorithm.team.setName("Greedy Team Using Projection Draft Position " + str(teamCounter+1))
			eachAlgorithm.team.setYear(testYear)
		else:
			eachAlgorithm.team.setName("Greedy Team Draft Position " + str(teamCounter+1))
			eachAlgorithm.team.setYear(testYear)
		teamCounter = teamCounter + 1

	#Run Test
	algoTester.runTest(testYear)
	runTime = time.time() - fileTimeStamp
	#Write outputs to results file
	resultsFile = open("results_"+str(testYear)+"_"+str(searchAlgoPosition)+"_"+str(fileTimeStamp)+".txt","w")
	print "Run Time Total: " + str(runTime)
	x = 0
	for a in algoTester.algorithms:
		x = x + 1
		resultsFile.write("Algorithm Name: " + str(a.team.name) + "\n")
		resultsFile.write("Member total points: " + str(a.team.getTotalPoints()) + "\n")
		resultsFile.write("Member starter points: " + str(a.team.getStarterPoints()) + "\n")
		resultsFile.write("Next Year Starter Points: " + str(a.team.getStarterPointsNextYear()) + "\n")
		a.team.resetTeam()


########## INPUTS CHANGE THESE IN ORDER TO RUN TEST #############
for eachPosition in range(1,11):
	for eachYear in range (2002,2013):
		print "Running test on year " + str(eachYear) + " and in draft position " + str(eachPosition)
		runSimulation(eachPosition, eachYear)
