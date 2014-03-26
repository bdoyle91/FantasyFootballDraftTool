import html5lib
from bs4 import BeautifulSoup
import urllib2
import types
import unicodedata
import os
import re
import math

#Global Variable for working directory
DIRECTORY = os.getcwd()+'/SoupyFootballData.html'
DEFENSE_DIRECTORY = os.getcwd()+'/SoupyDefenseData.html'
PFF_DEFENSE_DIRECTORY = os.getcwd() + '/SoupyPFFDefenseData'


##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  exportToFile    **                                                                                     
#  
# Arguments: 	HTML ESPN-GO Stat Page               
# Function: 	Downloads HTML source data and transfers data into a HTML file   
# Returns: 		None
# 
#                                                                                                  
##########################################################################################

def exportToFile(directoryName, statPage):
    #Pull html source code from website                                                                     
    html = urllib2.urlopen(statPage)
    #Turn source code into BeautifulSoup object                                                             
    soup = BeautifulSoup(html)
    #Create file and allow it to be accessed by variable f                                                  
    f = open(directoryName, 'w')
    #Write soup to file                                                                                    
    f.write(str(soup))

##########################################################################################
#
# ** discoverStatTypes **
#
# Arguments: 	List of String from HTML-GO Stat Table
# Function: 	Finds out stat types listed on page and removes them
# Returns: 		List of string, Stat Types
#
#
##########################################################################################

def discoverStatTypes(playerData, firstPlayer, statType=""):
	#Record Stat Types in a list until we reach the first player in the table
	type_List = []
	for item in playerData:
		#increment until we find our expected first player
		if str(item) == firstPlayer:
			break
	#handles unneeded rows in misc scorers
		if (item!="TOUCHDOWNS" or item!="SCORING"):
			type_List.append(item)
	if statType=="MiscScorers" or statType=="Kicking":
		del type_List[0]
		del type_List[0]
	return type_List

##########################################################################################
#
# ** removeStatTypes **
#
# Arguments: 	List of String from HTML-GO Stat Table
# Function: 	Finds out stat types listed on page and removes them
# Returns: 		None
#
#
##########################################################################################

def removeStatTypes(playerData, typeList):
	#Remove each stat-type from the list
	for item in typeList:
		while item in playerData: playerData.remove(item)

	#handles extra rows in misc scorers page
	while "TOUCHDOWNS" in playerData: playerData.remove("TOUCHDOWNS")
	while "SCORING" in playerData: playerData.remove("SCORING")
	while "FIELD GOALS" in playerData: playerData.remove("FIELD GOALS")
	while "EXTRA POINTS" in playerData: playerData.remove("EXTRA POINTS")

##########################################################################################
#
# ** separatePlayerPosition **
#
# Arguments:	List of String from HTML-GO Stat Table, location of player name in table
#				structure, typeList Must be done BEFORE addition of POS to typelist
# Function: 	Separates Player Name from Position
# Returns: 		None
#
#
##########################################################################################

def separatePlayerPosition(playerData, typeList, position):
	# print "playerData"
	# print playerData
	# print "typelist"
	# print typeList
	# print "position"
	# print position
	numberOfTypes = len(typeList)
	numberOfPlayers = len(playerData)/numberOfTypes
	for i in range(0, numberOfPlayers):
		#i+position = original offset plus insertion offset
		#i*numberOfTypes = space each player has taken up thus far
		# print "i: " + str(i)
		player = playerData[i+position+(i*numberOfTypes)]
		# print "player 1"
		# print player
		#Split position and name, change name/position field to just name, insert position

		player = player.rsplit(",")

		# print "len(player)"
		# print len(player)

		# print "player 2"
		# print "player" + str(player)
		playerData[i+position+(i*numberOfTypes)]=player[1]
		playerData.insert(i+position+(i*numberOfTypes),player[0])



##########################################################################################
#
# ** parseToString **
#
# Arguments: 	HTML ESPN-GO Stat Page
# Function: 	Parses text from HTML file into a list of string
# Returns: 		Player Data
#
#
##########################################################################################

def parseToString(statPage):
	exportToFile(DIRECTORY, statPage)

    # Replace first argument to open() with whatever file holds the html source code
	h = open(DIRECTORY, 'r+')
	s = h.read()
	h.close()
	# Turns string s into a BeautifulSoup object
	soup = BeautifulSoup(s)

    # Searches the html for the tbody tag, which contains the entire table
	tbody_tag = soup.tbody
	try:	
		td_list = tbody_tag.find_all_next("td")
	    # Creates a list of everything in table
		contents_list = []

		#for each <td> tag, get the value in the tags
		for tds in td_list:
			contents_list.append(tds.get_text())
		stringContents = []

		#encode in utf
		for eachItem in contents_list:
			stringContents.append(eachItem.encode('utf-8'))
		return stringContents
	except Exception, e:
		return ""

##########################################################################################
#
# ** parseDefensePage **
#
# Arguments: 	Pro-Football-Reference Stat Page
# Function: 	Parses text from HTML file into a list of string
# Returns: 		Player Data
#
#
##########################################################################################

def parseDefensePage(directoryName, statPage):
	exportToFile(directoryName, statPage)
	# Replace first argument to open() with whatever file holds the html source code
	h = open(directoryName, 'r+')
	s = h.read()
	h.close()
	# Turns string s into a BeautifulSoup object
	soup = BeautifulSoup(s)

	teamStatsTable = soup.find("table", id="team_stats")
	i = 0
	for string in teamStatsTable.stripped_strings:
		i = i + 1
		if i == 63: 
			pointsAllowed = string
			# print pointsAllowed
		elif i == 64:
			yardsAllowed = string
			# print yardsAllowed
		# print repr(string)

	defenseAndFumblesTable = soup.find("table", id="defense")
	kickAndPuntReturnTable = soup.find("table", id="returns")

##########################################################################################
#
# ** parseESPNDefensePage **
#
# Arguments: 	Pro-Football-Reference Stat Page
# Function: 	Parses text from HTML file into a list of string
# Returns: 		Player Data
#
#
##########################################################################################

# def parseESPNDefensePage(directoryName, statPage):
# 	exportToFile(directoryName, statPage)
# 	# Replace first argument to open() with whatever file holds the html source code
# 	h = open(directoryName, 'r+')
# 	s = h.read()
# 	h.close()
# 	# Turns string s into a BeautifulSoup object
# 	soup = BeautifulSoup(s)
# 	tbody_tag = soup.tbody
# 	td_list = tbody_tag.find_all_next("td")
# 	i = 0
# 	# for string in statsTable.stripped_strings:
# 	# 	# i = i + 1
# 	# 	# if i == 63: 
# 	# 	# 	pointsAllowed = string
# 	# 	# 	print pointsAllowed
# 	# 	# elif i == 64:
# 	# 	# 	yardsAllowed = string
# 	# 	# 	print yardsAllowed
# 	# 	print repr(string)
# 	print td_list

# 	defenseAndFumblesTable = soup.find("table", id="defense")
# 	kickAndPuntReturnTable = soup.find("table", id="returns")


##########################################################################################
#
# ** fixAllDataCol **
#
# Arguments: 	Data ripped from webpages
# Function: 	Removes any text that would break SQL Lite Commands
# Returns: 		Data in list of string format
#
#
##########################################################################################
def fixAllDataCol(dataList, statType=""):
	i=0
	for data in dataList:
		data = data.replace('20', 'TWENTY')
		data = data.replace('1DN', 'FIRST_DOWNS')
		data = data.replace('2PT', 'TWO_POINT_CONVS')
		if statType == "Defense":
			data = data.replace('SOLO', 'TACKLES_SOLO')
			data = data.replace('AST', 'TACKLES_AST')
			data = data.replace('TOTAL', 'TACKLES_TOTAL')
			data = data.replace('YDSL', 'SACKS_YARDSLOST')
			data = data.replace('PD', 'PASSES_DEFENDED')
			data = data.replace('YDS', 'INT_YARDS')
			data = data.replace('LONG', 'INT_LONG')
			data = data.replace('FF', 'FORCED_FUMBLES')
			data = data.replace('REC', 'FUMBLES_RECOVERED')
			data = data.replace('TD', 'FUMBLE_RECOVERY_TD')
		data = re.sub('[+]', '_PLUS', data)
		data = re.sub('\'', '', data)
		testList = data.split("/")
		for test in testList:
			if len(testList)==2:
				data = testList[0] + "_PER_" + testList[1]
		dataList[i] = data
		i = i + 1
	if statType == "Defense":
		dataList.remove("FUMBLE_RECOVERY_TD")
		dataList.insert(11, "INT_TD")
	return dataList

##########################################################################################
#
# ** fixAllDataPlayer **
#
# Arguments: 	Data ripped from webpages
# Function: 	Removes any text that would break SQL Lite Commands
# Returns: 		Data in list of string format
#
#
##########################################################################################
def fixAllDataPlayer(dataList):
	i=0
	for data in dataList:
		data = re.sub('\'', '', data)
		data = re.sub(',', '', data)
		dataList[i] = data
		i = i + 1
	return dataList

##########################################################################################
#
# ** getAllPages **
#
# Arguments: 	Default setup of a ESPN-GO stat page
# Function: 	Parses text from HTML file into a list of string
# Returns: 		Player Data
#
#
##########################################################################################

def getAllPages(statPage, statType=""):
	count = 0
	allPlayers = []
	while True:
		#incremement the regular expression in the link
		players = parseToString(statPage+str(1+count*40))
		#if no data in list, no players remain break loop
		if not players:
			break
		#Remove the state type information sprinkled in the list and store in secondary list
		statTypeList = discoverStatTypes(players, str(1+(count*40)), statType)
		removeStatTypes(players, statTypeList)
		#handle extra column in Misc page 
		if statType=="MiscScorers":
			for i in range(0, int(math.ceil((len(players)/len(statTypeList))/10.0))):
				players.pop(i*(len(statTypeList)*10))
		#Call function to split the string which includes both player and position
		separatePlayerPosition(players, statTypeList, 1)
		fixAllDataPlayer(players)
		
		#Append new list of string to total list
		allPlayers += players

		#Increment Counter
		count = count + 1
	return allPlayers

##########################################################################################
#
# ** getCorrectPositions **
#
# Arguments: 	Default setup of a ESPN-GO stat page
# Function: 	Parses column from HTML file into a list of string fixes all columns
# Returns: 		Column Data
#
#
##########################################################################################

def getCorrectPositions(statPage, statType=""):
 	players = parseToString(statPage)
 	count = 0
 	statTypeList = discoverStatTypes(players, str(1+(count*40)), statType)
 	if statType == "MiscScoring":
 		statTypeList.pop(0)
 		statTypeList.pop(1)
 		statTypeList.pop(2)
 	# Insert POS 
 	if statType != "Defense" and statType != "Defense Scoring":
 		statTypeList.insert(2, "POS")
 	if statType == "Defense":
 		statTypeList.pop(0)
 		statTypeList.pop(0)
 		statTypeList.pop(0)
 		statTypeList.pop(0)
 		statTypeList.pop(0)
 	elif statType == "Defense Scoring":
 		statTypeList.pop(0)
 		statTypeList.pop(0)
 		statTypeList.pop(0)
 	statTypeList = fixAllDataCol(statTypeList, statType)
 	return statTypeList

##########################################################################################
#
# ** getDefensivePtsYds **
#
# Arguments: 	Pro-Football-Reference statPage 
# Function: 	Returns the number of Fantasy Points that a team's defense earns in a season,
#					and the number total yar
# Returns: 		The sum of the fantasy points
#
#
##########################################################################################

def getDefensivePtsYds(statPage):
	exportToFile(PFF_DEFENSE_DIRECTORY, statPage)

    # Replace first argument to open() with whatever file holds the html source code
	h = open(PFF_DEFENSE_DIRECTORY, 'r+')
	s = h.read()
	h.close()
	# Turns string s into a BeautifulSoup object
	soup = BeautifulSoup(s)

    # Searches the html for the tbody tag, which contains the entire table
	teamStatsTable = soup.find("table", id="team_gamelogs")
	td_list = teamStatsTable.find_all_next("td")

	textList = []
	for item in td_list:
		textList.append(item.get_text())

	x = 0
	for item in textList:
		if item == "Playoffs":
			index = x
			for i in range(index, len(textList)):
				textList.pop(len(textList) - 1)
		x = x + 1
	# print textList

	x = 0
	fantasyPoints = 0
	for item in textList:
		if item == '':
			x = x + 1
			continue
		if (x%24) == 10:
			val = int(item)
			if val == 0:
				fantasyPoints = fantasyPoints + 5
			elif val <= 6:
				fantasyPoints = fantasyPoints + 4
			elif val <= 13:
				fantasyPoints = fantasyPoints + 3
			elif val <= 17:
				fantasyPoints = fantasyPoints + 1
			elif val <= 27:
				fantasyPoints = fantasyPoints + 0
			elif val <= 34:
				fantasyPoints = fantasyPoints - 1
			elif val <= 45:
				fantasyPoints = fantasyPoints - 3
			else:
				fantasyPoints = fantasyPoints - 5
			

		if (x%24) == 17:
			val = int(item)
			if val <= 100:
				fantasyPoints = fantasyPoints + 5
			elif val <= 199:
				fantasyPoints = fantasyPoints + 3
			elif val <= 299:
				fantasyPoints = fantasyPoints + 2
			elif val <= 349:
				fantasyPoints = fantasyPoints + 0
			elif val <= 399:
				fantasyPoints = fantasyPoints - 1
			elif val <= 449:
				fantasyPoints = fantasyPoints - 3
			elif val <= 499:
				fantasyPoints = fantasyPoints - 5	
			elif val <= 549:
				fantasyPoints = fantasyPoints - 6
			else:
				fantasyPoints = fantasyPoints - 7
		x = x + 1
		if (x/24) >= 17:
			break
	
	return fantasyPoints
