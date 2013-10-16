import html5lib
from bs4 import BeautifulSoup
import urllib2
import types
import unicodedata
import os

DIRECTORY = os.getcwd()+'/SoupyFootballData.html'



##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  exportToFile    **                                                                                     
#  
# Arguments: HTML ESPN-GO Stat Page               
# Function: Downloads HTML source data and transfers data into a HTML file   
# Returns: None
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
    # Write soup to file                                                                                    
    f.write(str(soup))




##########################################################################################
#
# ** findPosition **
#
# Arguments: "Player Name, Position" string
# Function: cuts final two characters off of string
# Returns: Player's position
#
#
##########################################################################################

def findPosition(player):
	splitp = player.split()
	pos = splitp[len(splitp)-1]
	print pos



##########################################################################################
#
# ** parseToString **
#
# Arguments: HTML ESPN-GO Stat Page
# Function: Parses text from HTML file into a list of string
# Returns: Player Data
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
	playerList = soup.find_all("td", class_= "playertablePlayerName")
	tableList = soup.find_all("td", class_="playertableStat")
	x = 0
	del tableList[0:15]
    # Creates a list of everything
	contents_list = []
	playerContents = []
	stringContents = []
	players = []
	for item in playerList:
		playerContents.append(item.get_text())
	for eachItem in tableList:
		stringContents.append(eachItem.get_text())
	qbs = []
	while(len(playerContents)>0):
		temp = playerContents.pop(0) + "," + stringContents.pop(0) + "," + stringContents.pop(0) + "," + stringContents.pop(0) + "," + stringContents.pop(0) + "," + stringContents.pop(0) + "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)+ "," + stringContents.pop(0)
		players.append(temp)
	return players
