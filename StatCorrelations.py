import sqlite3 as lite
import math
import operator
import traceback

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  statPull  **                                                                                     
#  
# Arguments: 	Name of table (not including _yyyy), Name of column in table, Year
# Function: 	Selects a stat to compare to the next season's fantays points, stores all 
#					data from that column, along with the associated player's name, in a list
# Returns: 		List of tuples of form (playerName, stat, rank)
# 
#
#                                                                                                  
##########################################################################################

def statPull(tableName, columnName, position, year):
	conn = lite.connect('ESPN.db')
	conn.text_factory = str # set sqlite3 connection to use unicode instead of 8-bit byte strings. 
	with conn:
		c = conn.cursor()	# Defines cursor
		commandString = "SELECT PLAYER, " + str(columnName) + " FROM " + tableName + "_" + str(year) + " WHERE POS=\"" + position + "\";"
		# print commandString
		c.execute(commandString) # Create the table
		dictionary = {}
		tupleList = list(set(c.fetchall()))
		newTupleList = []
		for tuple in tupleList:
			newTupleList.append((tuple[0], int(tuple[1])))
		dictionary.update(newTupleList)
		# print "DICT: " + str(dictionary)
		sortedDict = sorted(dictionary.iteritems(), key=operator.itemgetter(1))
		correctlySortedDict = list(reversed(sortedDict))
		correctlySortedDict = addRankToTuple(correctlySortedDict)
		# print "List sorted by top players: " + str(correctlySortedDict)
		if tableName != "FantasyPoints":
			if position.strip() == "QB" or position.strip() == "TE" or position.strip() == "PK":
				correctlySortedDict = correctlySortedDict[:15]
			elif position.strip() == "RB" or position.strip() == "WR":
				correctlySortedDict = correctlySortedDict[:50]
		# print "Top 15 players: " + str(correctlySortedDict)
		conn.commit() # MAY NOT NEED THIS
	conn.close()
	print "\n"
	return correctlySortedDict

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  addRankToTuple  **                                                                                     
#  
# Arguments: 	list of tuples
# Function: 	Simply creates a new list from the given one, with an extra "rank" index in each tuple
# Returns: 		List of lists of form (playerName, stat, rank)
# 
#
#                                                                                                  
##########################################################################################

def addRankToTuple(listOfTuples):
	newList = []
	# i = 0
	for item in listOfTuples:
		# i = i + 1
		# temp = item[0], item[1], i
		newList.append(item[0])
	return newList

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  calculateCoefficient  **                                                                                     
#  
# Arguments: 	list of tuples
# Function: 	Calculates the rank correlation coefficients 
# 					between a stat and the next year's fantasy points for that player
# Returns: 		correlation coeffiecient (number between -1 and 1)
# 
#
#                                                                                                  
##########################################################################################

def calculateCoefficient(statsList, pointsList):
	sumDSquared = 0
	i = 0
	print statsList
	print "\n\n\n"
	print pointsList
	print "\n\n\n"
	for item in statsList:
		try:
			pli = pointsList.index(item)
			print "pli: " + str(pli)
		except ValueError:
			continue
		print statsList[i]
		dSquared = pli - i
		print "dSquared: " + str(dSquared)
		print "\n"
		sumDSquared = math.pow(dSquared, 2)
		i = i + 1
	print "sumDSquared: " + str(sumDSquared)
	print "\n"
	print "i: " + str(i)
	spearman = 1 - ((6 * sumDSquared) / (i * (math.pow(i, 2) - 1)))
	print "Spearman coefficient " + str(spearman)
	if (spearman < -1) or (spearman > 1):
		traceback.print_stack()
	return spearman

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  findAverageCoefficient  **                                                                                     
#  
# Arguments: 	string (name of stat), string (name of table to find that stat in), 
#					string (player's position)
# Function: 	Runs calculateCoefficient on every year that we have stats for, calculates
#					average coefficient
# Returns: 		average correlation coefficient
# 
#
#                                                                                                  
##########################################################################################

def findAverageCoefficient(stat, tableName, position):
	coefficientSum = 0
	print "Stat: " + str(stat)
	for year in range(2002, 2013):
		calcCo = calculateCoefficient(statPull(tableName, stat, position, year), statPull("FantasyPoints", "Points", position, year + 1))
		coefficientSum = coefficientSum + calcCo
		print "calcCo: "  + str(calcCo) + " for " + str(year)
	coefficientAvg = coefficientSum / 11
	print "coefficientAvg: " + str(coefficientAvg)
	return coefficientAvg


##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  findAllAverages  **                                                                                     
#  
# Arguments: 	list of tuples (stat, table, position)
# Function: 	Runs findAverageCoefficient on every stat for each position
# Returns: 		dictionary that maps Position-Stat to Correlation
# 
#
#                                                                                                  
##########################################################################################

def findAllAverages(listOfTuples):
	cDict = {}

	for t in listOfTuples:
		key = str(t[2]) + "-" + str(t[0])
		cDict[key] = findAverageCoefficient(t[0], t[1], t[2])



def createListOfTuples():
	list = []


# calculateCoefficient(statPull("Passing", "COMP", " QB", 2011), statPull("FantasyPoints", "Points", " QB", 2012))
findAverageCoefficient("COMP", "Passing", " QB")
