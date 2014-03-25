import ScrapingFunctions
import os

DEFENSE_DIRECTORY = os.getcwd()+'/SoupyDefenseData.html'
PFF_DEFENSE_DIRECTORY = os.getcwd() + '/SoupyPFFDefenseData'

ScrapingFunctions.getDefensivePtsYds("http://www.pro-football-reference.com/teams/phi/2013.htm")