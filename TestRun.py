from algorithmTester import *
from LocalSearchAlgorithm import *
from LeagueTeams import *
import time
import os

########## INPUTS CHANGE THESE IN ORDER TO RUN TEST #############
searchAlgoPosition = 10
testYear = 2011

#Construct Results file
fileTimeStamp = time.time()
resultsFile = open("results_"+str(testYear)+"_"+str(searchAlgoPosition)+"_"+str(fileTimeStamp)+".txt","w")

#Construct algorithm list
algoTester = algorithmTester()
for teamNum in range(0, NUMBER_OF_TEAMS):
	if teamNum == (searchAlgoPosition - 1):
		algoTester.algorithms.append(LocalSearchAlgorithm("LOCALSEARCH", NUMBER_OF_TEAMS, teamNum))
	else:
		algoTester.algorithms.append(GreedyByPositionAlgorithm("Greedy"))

#Organize team instances
teamCounter = 0
for eachAlgorithm in algoTester.algorithms:
	eachAlgorithm.team = TEAM_LIST[teamCounter]
	if teamCounter == (searchAlgoPosition - 1):
		eachAlgorithm.team.setName("LocalSearch Team Draft Position " + str(teamCounter+1))
	else:
		eachAlgorithm.team.setName("Greedy Team Draft Position " + str(teamCounter+1))
	teamCounter = teamCounter + 1

#Run Test
algoTester.runTest(testYear)

#Write outputs to results file
x = 0
for a in algoTester.algorithms:
	x = x + 1
	resultsFile.write("Algorithm Name: " + str(a.team.name) + "\n")
	resultsFile.write("Member total points: " + str(a.team.getTotalPoints()) + "\n")
	resultsFile.write("Member starter points: " + str(a.team.getStarterPoints()) + "\n")

