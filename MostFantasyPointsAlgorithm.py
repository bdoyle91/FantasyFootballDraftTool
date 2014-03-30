import teamClass
import sqlite3 as lite

# Maximum Number of players from each position allowed on a roster
MAX_QBS_PER_TEAM = 4
MAX_RBS_PER_TEAM = 8
MAX_WRS_PER_TEAM = 8
MAX_TES_PER_TEAM = 3
MAX_DSTS_PER_TEAM = 3
MAX_KS_PER_TEAM = 3

TEAM_SIZE = 16

##########################################################################################
#
# GLOBAL_FUNCTION: CALL_SQL_COMMAND
#		
# ARGS:			Database Name, Command String
# Returns:		Returns SQL Cursor
#
##########################################################################################

def CALL_SQL_COMMAND(database, command):
	conn = lite.connect(database)
	c = conn.cursor()
	c.execute(command)
	conn.close()
	return c

CALL_SQL_COMMAND("ESPN.db", "SELECT Player, Pos, Points FROM DraftList_2013")
