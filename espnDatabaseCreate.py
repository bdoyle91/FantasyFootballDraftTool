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
	while(len(playerList)!=0):
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

def createESPNTable(statPage, nameOfTable, tableType=""):
	#Get all the column info that will be used for this table with all fixing
	#to be in userable SQL formats
	statTypeList = scrapingFunctions.getCorrectPositions(statPage, tableType)

	#
	if tableType=="MiscScoring":
		allPlayers = scrapingFunctions.getAllPages(statPage, "MiscScorers")
	else:
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
# ** createFantasyPointTables **
#
# Arguments: 	name of all SQL tables containing player information. Year of information
#				to be implemented once multiple years of data are stored.
# Function: 	Calculates approximate fantasy point totals for each player based on
#				season aggregates. Totals will not be exact due to season vs. weekly
#				calculations, however can be used with accuracy of max 16 point difference.
#				Then creates a FantasyPoints table in ESPN.db to be referenced when testbenching.		
# Returns: 		None
#
#
##########################################################################################

def createFantasyPointTables(tableNames, year=""):
	#initalize the allPlayers list of string
	allPlayers =[]

	#connect to our existed database and delete FantasyPoints table if it already exists
	conn = lite.connect('ESPN.db')
	dropTableCommand = "DROP TABLE IF EXISTS FantasyPoints_"+str(year)
	c = conn.cursor()
	c.execute(dropTableCommand)	# Recreate table so we don't have to keep deleting the .db file
	conn.text_factory = str

	#Create FantasyPoints Table
	statTypeList = ["Player, Pos, Points"]
	c.execute(addHeadersToTable(statTypeList, "CREATE TABLE FantasyPoints_"+str(year)+" ("))
	conn.close()

	#Get all players from all tables, do not record any players twice
	for name in tableNames:
		command = "SELECT PLAYER, POS FROM " + str(name)  + "_" + str(year)
		conn = lite.connect('ESPN.db')
		c = conn.cursor()
		c.execute(command)
		players = c.fetchall()
		collision = 0
		for player in players:
			#check if player has allready been appended to list
			for allPlayer in allPlayers:
				if allPlayer == player[0]:
					collision = 1
			#if no collision, add player to allPlayers
			if collision == 0:
				allPlayers.append(player)

			#if collision was detected, return collision back to zero for next player
			else:
				collision = 0
		conn.close()
	try:
		for player in allPlayers:
			fantasyPoint = 0
			for name in tableNames:
				conn = lite.connect('ESPN.db')
				c = conn.cursor()
				cols = []
				command = "SELECT * FROM " + str(name) + "_" + str(year)
				c.execute(command)
				for item in c.description:
					cols.append(item[0])
				for position in range(4, len(cols)):
					cols[position] = name + "_" + cols[position]
				command = "SELECT * FROM " + str(name)  + "_" + str(year) +  " WHERE PLAYER= '" + str(player[0]) + "'"		
				c.execute(command)
				stats = c.fetchall()
				#check to see if player existed in table
				if stats:
					counter = 0
					#Add fantasy points for ESPN default stats
					for column in cols:
						if column == "Passing_YDS":
							fantasyPoint = fantasyPoint + (int(stats[0][counter])/25)
						if column == "Passing_TD":
							fantasyPoint = fantasyPoint + (int(stats[0][counter])*4)
						if column == "Passing_INT":
							fantasyPoint = fantasyPoint - (int(stats[0][counter])*2)
						if column == "Rushing_YDS":
							fantasyPoint = fantasyPoint + (int(stats[0][counter])/10)
						if column == "Rushing_TD":
							fantasyPoint = fantasyPoint + (int(stats[0][counter])*6)
						if column == "Rushing_FUM":
							fantasyPoint = fantasyPoint - (int(stats[0][counter])*2)
						if column == "Receiving_YDS":
							fantasyPoint = fantasyPoint + (int(stats[0][counter])/10)
						if column == "Receiving_TD":
							fantasyPoint = fantasyPoint + (int(stats[0][counter])*6)
						if column == "Receiving_FUM":
							fantasyPoint = fantasyPoint - (int(stats[0][counter])*2)
						counter = counter + 1
			#Insert player's calculated fantasy point into SQL Table
			commandString = "INSERT INTO FantasyPoints_"+str(year)+ " VALUES (\'"+player[0]+"\',\'"+player[1]+"\', \'"+str(fantasyPoint)+"\')"
			conn.text_factory = str
			c.execute(commandString)
			conn.commit()
			conn.close()
		#If end of code reached successfully all entries successfully added
		print "FantasyPoints_"+str(year)+" Table Created"	
		
	#Print error of exception raised		
	except Exception, e:
		print "Error when attempting to create FantasyPoints_"+str(year)+" SQL Table:"
		raise

##########################################################################################
#
# ** MAIN **
#
# Function: 	Creates all SQL Tables that are to be used by our algorithim
#			
# 
#
##########################################################################################

#Create Misc Scoring Table
for year in range(2002, 2014):
	if year == 2013:
		MiscScoring_Page = "http://espn.go.com/nfl/statistics/player/_/stat/scoring/seasontype/2/qualified/false/count/"
	else:
		MiscScoring_Page ="http://espn.go.com/nfl/statistics/player/_/stat/scoring/sort/totalPoints/year/"+str(year)+"/qualified/false/count/"
	print MiscScoring_Page
	createESPNTable(MiscScoring_Page, "MiscScoring_"+str(year), "MiscScoring")

#Create Passing Table
for year in range(2002, 2014):
	if year == 2013:
		Passing_Page = "http://espn.go.com/nfl/statistics/player/_/stat/passing/sort/passingYards/seasontype/2/qualified/false/count/"
	else:
		Passing_Page="http://espn.go.com/nfl/statistics/player/_/stat/passing/sort/passingYards/year/"+str(year)+"/seasontype/2/qualified/false/count/"
	createESPNTable(Passing_Page, "Passing_"+str(year))

#Create Rushing Table
for year in range(2002, 2014):
	if year == 2013:
		Rushing_Page = "http://espn.go.com/nfl/statistics/player/_/stat/rushing/seasontype/2/qualified/false/count/"
	else:
		Rushing_Page="http://espn.go.com/nfl/statistics/player/_/stat/rushing/sort/rushingYards/year/"+str(year)+"/seasontype/2/qualified/false/count/"
	createESPNTable(Rushing_Page, "Rushing_"+str(year))

#Create Receiving Table
for year in range(2002, 2014):
	if year == 2013:
		Receiving_Page = "http://espn.go.com/nfl/statistics/player/_/stat/receiving/seasontype/2/qualified/false/count/"
	else:
		Receiving_Page="http://espn.go.com/nfl/statistics/player/_/stat/receiving/sort/receivingYards/year/"+str(year)+"/seasontype/2/qualified/false/count/"
	createESPNTable(Receiving_Page, "Receiving_"+str(year))

#Create FantasyPoints Table
for year in range(2002, 2014):
	i=0
	tableNames = ["Passing","Rushing","Receiving"]
	createFantasyPointTables(tableNames, year)

###### MORE TABLES TO BE ADDED ######

