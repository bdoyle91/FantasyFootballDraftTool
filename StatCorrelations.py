import sqlite3 as lite
import math
import operator

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
		sumDSquared = math.pow(dSquared, 2)
		i = i + 1
	print "sumDSquared: " + str(sumDSquared)
	spearman = 1 - ((6 * sumDSquared) / (i * (math.pow(i, 2) - 1)))
	# print spearman


calculateCoefficient(statPull("Passing", "COMP", " QB", 2011), statPull("FantasyPoints", "Points", " QB", 2012))
