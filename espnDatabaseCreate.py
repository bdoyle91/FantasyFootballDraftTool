import scrapingFunctions
import sqlite3 as lite

##########################################################################################
#
# ** addHeadersToTable **
#
# Arguments: 	List of column headers, input string for the headers to be appended to
# Function: 	Concatenates all stat types for a table into one string,
#					to be called by the sqlite "execute" command
# Returns: 		The command string
#
#
##########################################################################################

def addHeadersToTable(listOfHeaders, stringOfHeaders, ):
	for title in listOfHeaders:
		stringOfHeaders = stringOfHeaders + title + " TEXT, "
	newString = stringOfHeaders[:len(stringOfHeaders)-2]
	newString = newString + ")"
	return newString

##########################################################################################
#
# ** getSQLStr **
#
# Arguments: 	List of column headers, input string for the headers to be appended to
# Function: 	
# Returns: 		SQL String of Question Marks to be used by execute many function
#
#
##########################################################################################

def getSQLStr(listOfHeaders):
	newString = ""
	listLength = len(listOfHeaders)
	i=1
	while i<listLength:
		newString = newString + "?,"
		i = i + 1
	newString = newString + "?"
	return newString

##########################################################################################
#
# ** listToListOfLists **
#
# Arguments: 	List of player data, list of stat types, list of lists of player data
# Function: 	Turns a list of player data into a list of player tuples
# Returns: 		List of tuples of player data for use in executemany sqlite command
#
#
##########################################################################################

def listToListOfLists(playerList, statTypeList, listOfLists):
	for x in playerList:
		subList = []

		while ((len(subList) < len(statTypeList)) and (len(playerList) != 0)):
			subList.append(playerList.pop(0))

		listOfLists.append(subList)

	return listOfLists

##########################################################################################
#
# ** createESPNTable **
#
# Arguments: 	statPage URL to create Table from, name of table to be created
# Function: 	Rips NFL Player info from ESPN-GO stat page and creates
#				SQL table from them				
# Returns: 		None
#
#
##########################################################################################

def createESPNTable(statPage, nameOfTable):
	#Get all the column info that will be used for this table with all fixing
	#to be in userable SQL formats
	statTypeList = scrapingFunctions.getCorrectPositions(statPage)

	#
	allPlayers = scrapingFunctions.getAllPages(statPage)
	listOfLists = []
	listOfLists = listToListOfLists(allPlayers, statTypeList, listOfLists)
	SQLString = getSQLStr(statTypeList)
	tableHeaders = "CREATE TABLE " + nameOfTable + "("
	dbFileName = "ESPN.db"
	conn = lite.connect('ESPN.db')
	conn.text_factory = str # set sqlite3 connection to use unicode instead of 8-bit byte strings. 
							#Added to resolve an error with the c.executemany line below.
	with conn:
		c = conn.cursor()	# Defines cursor
		dropTableCommand = "DROP TABLE IF EXISTS " + nameOfTable
		c.execute(dropTableCommand)	# Recreate table so we don't have to keep deleting the .db file
		c.execute(addHeadersToTable(statTypeList, tableHeaders)) # Create the table
		commandString = "INSERT INTO " + nameOfTable + " VALUES(" + SQLString + ")"
		c.executemany(commandString, listOfLists) # Add all values for each player into table
		
		print nameOfTable + " Table Created"
		conn.commit()
	conn.close()


##########################################################################################
#
# ** MAIN **
#
# Function: 	Creates all SQL Tables that are to be used by our algorithim
#			
# 
#
##########################################################################################

#Create Passing Table
Passing_Page = "http://espn.go.com/nfl/statistics/player/_/stat/passing/sort/passingYards/seasontype/2/qualified/false/count/"
createESPNTable(Passing_Page, "Passing")

#Create Rushing Table
Rushing_Page = "http://espn.go.com/nfl/statistics/player/_/stat/rushing/seasontype/2/qualified/false/count/"
createESPNTable(Rushing_Page, "Rushing")

#Create Receiving Table
Receiving_Page = "http://espn.go.com/nfl/statistics/player/_/stat/receiving/seasontype/2/qualified/false/count/"
createESPNTable(Receiving_Page, "Receiving")


###### MORE TABLES TO BE ADDED ######

# MiscScoring_Page = "http://espn.go.com/nfl/statistics/player/_/stat/scoring/seasontype/2/qualified/false/count/"
# MiscScorers = scrapingFunctions.getAllPages(MiscScoring_Page,"MiscScorers")
# print('\n\n\n\n-------------- MISC SCORING --------------------')
# print(MiscScorers)

