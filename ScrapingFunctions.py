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

def exportToFile(statPage):
    #Pull html source code from website                                                                     
    html = urllib2.urlopen(statPage)
    #Turn source code into BeautifulSoup object                                                             
    soup = BeautifulSoup(html)
    #Create file and allow it to be accessed by variable f                                                  
    f = open(DIRECTORY, 'w')
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
		if item!="TOUCHDOWNS" or item!="SCORING" and statType!="MiscScorers":
			type_List.append(item)
	if statType=="MiscScorers":
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
	numberOfTypes = len(typeList)
	numberOfPlayers = len(playerData)/numberOfTypes
	for i in range(0, numberOfPlayers):
		#i+position = original offset plus insertion offset
		#i*numberOfTypes = space each player has taken up thus far
		player = playerData[i+position+(i*numberOfTypes)]
		#Split position and name, change name/position field to just name, insert position
		player = player.rsplit(",")
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
	exportToFile(statPage)

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
# ** fixAllDataCol **
#
# Arguments: 	Data ripped from webpages
# Function: 	Removes any text that would break SQL Lite Commands
# Returns: 		Data in list of string format
#
#
##########################################################################################
def fixAllDataCol(dataList):
	i=0
	for data in dataList:
		data = data.replace('20', 'TWENTY')
		data = data.replace('1DN', 'FIRST_DOWNS')
		data = data.replace('2PT', 'TWO_POINT_CONVS')
		data = re.sub('[+]', '_PLUS', data)
		data = re.sub('\'', '', data)
		testList = data.split("/")
		for test in testList:
			if len(testList)==2:
				data = testList[0] + "_PER_" + testList[1]
		dataList[i] = data
		i = i + 1
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
 	statTypeList.insert(2, "POS")
 	statTypeList = fixAllDataCol(statTypeList)
 	return statTypeList
